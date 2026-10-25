#!/usr/bin/env python3
"""Generates the GitHub stats card from the GitHub API (run by the workflow).

    GITHUB_TOKEN=... USERNAME=... python3 scripts/generate_stats.py dist/stats.svg
"""
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import date
from xml.sax.saxutils import escape

from generate_svgs import MONO, SANS

# Languages left out of the breakdown (generated files and old notebooks).
EXCLUDE_LANGS = {"HTML", "CSS", "Jupyter Notebook"}
TOP_LANGS = 6

QUERY = """query($login: String!) { user(login: $login) {
  repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
    nodes { stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
      edges { size node { name color } } } } }
  contributionsCollection { totalCommitContributions contributionCalendar {
    totalContributions weeks { contributionDays { date contributionCount } } } }
  pullRequests { totalCount }
  issues { totalCount }
} }"""


def api(path, body=None):
    req = urllib.request.Request(
        f"https://api.github.com/{path}",
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
                 "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch(login):
    data = api("graphql", {"query": QUERY, "variables": {"login": login}})
    if "errors" in data:
        sys.exit(f"GraphQL error: {data['errors']}")
    user = data["data"]["user"]
    repos = user["repositories"]["nodes"]
    calendar = user["contributionsCollection"]["contributionCalendar"]

    langs, colors = Counter(), {}
    for repo in repos:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            if name not in EXCLUDE_LANGS:
                langs[name] += edge["size"]
                colors[name] = edge["node"]["color"] or "#8b949e"

    try:
        commits = api(f"search/commits?q=author:{login}&per_page=1")["total_count"]
        commits_label = "Total Commits"
    except Exception:
        commits = user["contributionsCollection"]["totalCommitContributions"]
        commits_label = "Commits (last year)"

    # Today may not have contributions yet, so it doesn't break the streak.
    days = [d for w in calendar["weeks"] for d in w["contributionDays"]
            if date.fromisoformat(d["date"]) <= date.today()]
    if days and days[-1]["contributionCount"] == 0:
        days = days[:-1]
    current = 0
    for d in reversed(days):
        if d["contributionCount"] == 0:
            break
        current += 1
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)

    stats = [
        ("Stars Earned", sum(r["stargazerCount"] for r in repos), "#ffd166"),
        (commits_label, commits, "#2de2e6"),
        ("Pull Requests", user["pullRequests"]["totalCount"], "#d2a8ff"),
        ("Issues", user["issues"]["totalCount"], "#7ee787"),
        ("Contributions (last year)", calendar["totalContributions"], "#58a6ff"),
        ("Streak (current / longest)", f"{current} / {longest} days", "#ff3cac"),
    ]
    total = sum(langs.values()) or 1
    top = [(name, size / total * 100, colors[name]) for name, size in langs.most_common(TOP_LANGS)]
    return stats, top


def render(stats, langs):
    W, H = 860, 250
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <linearGradient id="border" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">
    <stop offset="0" stop-color="#ff3cac"/><stop offset="0.5" stop-color="#784ba0"/><stop offset="1" stop-color="#2de2e6"/>
    <animateTransform attributeName="gradientTransform" type="rotate" from="0 {W / 2} {H / 2}" to="360 {W / 2} {H / 2}" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ff3cac"/><stop offset="1" stop-color="#2de2e6"/>
  </linearGradient>
  <filter id="soft" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<style>
  .in {{ animation: in 0.6s ease-out backwards; }}
  .bar {{ transform-box: fill-box; animation: grow 1.2s cubic-bezier(.2,.8,.2,1) backwards; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateX(-8px); }} }}
  @keyframes grow {{ from {{ transform: scaleX(0); }} }}
</style>
<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="14" fill="none" stroke="url(#border)" stroke-width="4" filter="url(#soft)" opacity="0.8"/>
<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="14" fill="#0d1117" stroke="url(#border)" stroke-width="1.5"/>
<line x1="430" x2="430" y1="30" y2="{H - 30}" stroke="#30363d"/>
<text x="30" y="46" font-family="{SANS}" font-size="20" font-weight="700" fill="url(#title)">GitHub Stats</text>
<text x="460" y="46" font-family="{SANS}" font-size="20" font-weight="700" fill="url(#title)">Top Languages</text>''']

    for i, (label, value, color) in enumerate(stats):
        y = 84 + i * 29
        out.append(f'<g class="in" style="animation-delay:{0.15 + i * 0.12:.2f}s">'
                   f'<circle cx="36" cy="{y - 5}" r="4" fill="{color}"/>'
                   f'<text x="50" y="{y}" font-family="{SANS}" font-size="14" fill="#8b949e">{escape(label)}</text>'
                   f'<text x="404" y="{y}" text-anchor="end" font-family="{MONO}" font-size="15" font-weight="700" '
                   f'fill="#e6edf3">{escape(str(value))}</text></g>')

    bar_w = 370
    for i, (name, pct, color) in enumerate(langs):
        y = 80 + i * 28
        delay = 0.3 + i * 0.12
        out.append(f'<g class="in" style="animation-delay:{delay:.2f}s">'
                   f'<text x="460" y="{y}" font-family="{SANS}" font-size="13" fill="#e6edf3">{escape(name)}</text>'
                   f'<text x="{460 + bar_w}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="12" '
                   f'fill="#8b949e">{pct:.1f}%</text></g>')
        out.append(f'<rect x="460" y="{y + 6}" width="{bar_w}" height="6" rx="3" fill="#21262d"/>')
        out.append(f'<rect class="bar" style="animation-delay:{delay + 0.2:.2f}s" x="460" y="{y + 6}" '
                   f'width="{max(bar_w * pct / 100, 6):.1f}" height="6" rx="3" fill="{color}"/>')

    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "stats.svg"
    stats, langs = fetch(os.environ["USERNAME"])
    with open(path, "w") as f:
        f.write(render(stats, langs) + "\n")
    print(f"wrote {path}")
