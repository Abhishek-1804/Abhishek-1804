#!/usr/bin/env python3
"""Generates the animated SVGs in assets/ used by the profile README.

Edit the content constants below, then re-run:
    python3 scripts/generate_svgs.py
"""
import random
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"
MONO = "'JetBrains Mono','Fira Code','SF Mono',Consolas,Menlo,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"

NAME = "Abhishek Deshpande"
GREETING = "hi there, i'm"
ROLES = [
    "Currently @ UiPath",
    "ex-SDE @ AWS",
    "DevOps & Cloud",
    "Automating all the things",
]

PROMPT = "abhishek@github:~$"
# Each entry is a typed command followed by its output lines; an output line is
# a list of (text, color) segments.
SESSION = [
    ("whoami", [
        [("Abhishek Deshpande", "#e6edf3"), (" // software developer, into devops", "#8b949e")],
        [("now ", "#8b949e"), ("@ UiPath", "#ff9e64"), ("   prev ", "#8b949e"), ("SDE @ AWS", "#ffd166")],
    ]),
    ("cat currently_learning.txt", [
        [("[kubernetes]", "#58a6ff"), ("  ", ""),
         ("[docker]", "#2de2e6"), ("  ", ""), ("[ci/cd]", "#f778ba"), ("  ", ""), ("[linux]", "#ffd166")],
    ]),
    ("node -e \"console.log([] == ![])\"", [
        [("true", "#7ee787")],
        [("// equal isn't always equal in JavaScript", "#8b949e")],
    ]),
    ("kubectl get pods -n life", [
        [("NAME              READY   STATUS", "#8b949e")],
        [("devops-journey    1/1     ", "#e6edf3"), ("Running", "#7ee787")],
        [("coffee-machine    0/1     ", "#e6edf3"), ("CrashLoopBackOff", "#ff7b72")],
    ]),
]


def discrete(attr, events, total):
    """SMIL animation that jumps to each (time, value) and loops every `total` seconds."""
    times = ";".join(f"{t / total:.5f}" for t, _ in events)
    values = ";".join(str(v) for _, v in events)
    return (f'<animate attributeName="{attr}" calcMode="discrete" dur="{total:.2f}s" '
            f'repeatCount="indefinite" keyTimes="{times}" values="{values}"/>')


def header():
    W, H, HORIZON = 1000, 320, 228
    rng = random.Random(1804)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']

    out.append(f'''<defs>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#05000f"/><stop offset="0.7" stop-color="#1d0638"/><stop offset="1" stop-color="#3a0a4f"/>
  </linearGradient>
  <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffe259"/><stop offset="0.5" stop-color="#ff7eb3"/><stop offset="1" stop-color="#b721ff"/>
  </linearGradient>
  <linearGradient id="name" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="0" spreadMethod="repeat">
    <stop offset="0" stop-color="#ff3cac"/><stop offset="0.33" stop-color="#ffd166"/>
    <stop offset="0.66" stop-color="#2de2e6"/><stop offset="1" stop-color="#ff3cac"/>
    <animate attributeName="x1" from="0" to="1000" dur="6s" repeatCount="indefinite"/>
    <animate attributeName="x2" from="1000" to="2000" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="fade" gradientUnits="userSpaceOnUse" x1="0" y1="{HORIZON}" x2="0" y2="{H}">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="1"/>
  </linearGradient>
  <mask id="gridFade"><rect y="{HORIZON}" width="{W}" height="{H - HORIZON}" fill="url(#fade)"/></mask>
  <mask id="sunStripes">
    <rect x="400" y="100" width="200" height="{HORIZON - 100}" fill="#fff"/>''')
    # Gaps through the lower half of the sun, thickening toward the horizon.
    y, gap = HORIZON - 52, 2
    while y < HORIZON:
        out.append(f'    <rect x="400" y="{y}" width="200" height="{gap}" fill="#000"/>')
        y += gap + 7
        gap += 1.5
    out.append(f'''  </mask>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="6" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="bigGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#sky)"/>''')

    for _ in range(80):
        x, y = rng.uniform(0, W), rng.uniform(0, HORIZON - 15)
        r = rng.choice([0.6, 0.8, 1.0, 1.3, 1.7])
        dur, begin = rng.uniform(1.8, 5), rng.uniform(0, 5)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff">'
                   f'<animate attributeName="opacity" values="0.15;1;0.15" dur="{dur:.2f}s" '
                   f'begin="-{begin:.2f}s" repeatCount="indefinite"/></circle>')

    # Shooting stars streak across every few seconds.
    for x0, y0, begin in [(140, 20, 0), (620, 10, 3.7)]:
        out.append(f'''<line x1="0" y1="0" x2="-70" y2="-28" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity="0">
  <animateTransform attributeName="transform" type="translate" values="{x0},{y0};{x0 + 260},{y0 + 104}" keyTimes="0;1" dur="7.4s" begin="{begin}s" repeatCount="indefinite" calcMode="spline" keySplines="0.2 0 0.4 1"/>
  <animate attributeName="opacity" values="0;1;0;0" keyTimes="0;0.04;0.12;1" dur="7.4s" begin="{begin}s" repeatCount="indefinite"/>
</line>''')

    out.append(f'''<circle cx="500" cy="{HORIZON}" r="78" fill="#ff7eb3" opacity="0.45" filter="url(#bigGlow)">
  <animate attributeName="opacity" values="0.3;0.6;0.3" dur="4s" repeatCount="indefinite"/>
</circle>
<circle cx="500" cy="{HORIZON}" r="66" fill="url(#sun)" mask="url(#sunStripes)"/>
<rect y="{HORIZON}" width="{W}" height="{H - HORIZON}" fill="#08000f"/>''')

    # Perspective grid: vertical lines converge on the vanishing point, horizontal
    # lines slide toward the viewer one slot per period so the loop is seamless.
    out.append(f'<g mask="url(#gridFade)" stroke="#f72585" stroke-width="1.4" filter="url(#glow)">')
    for i in range(-16, 17):
        out.append(f'<line x1="500" y1="{HORIZON}" x2="{500 + i * 75}" y2="{H}"/>')
    depth, dz, period, samples = H - HORIZON, 0.45, 1.1, 12
    for i in range(24):
        ys = []
        for s in range(samples + 1):
            z = 1 + (i - s / samples) * dz
            ys.append(f"{HORIZON + depth / z:.2f}" if z > 0.05 else f"{H + 400}")
        vals = ";".join(ys)
        out.append(f'<line x1="0" x2="{W}" y1="{ys[0]}" y2="{ys[0]}">'
                   f'<animate attributeName="y1" values="{vals}" dur="{period}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="y2" values="{vals}" dur="{period}s" repeatCount="indefinite"/></line>')
    out.append('</g>')
    out.append(f'<line x1="0" x2="{W}" y1="{HORIZON}" y2="{HORIZON}" stroke="#ff7eb3" stroke-width="2" filter="url(#glow)"/>')

    out.append(f'<text x="500" y="52" text-anchor="middle" font-family="{MONO}" font-size="18" '
               f'fill="#c9b6ff" letter-spacing="3">{escape(GREETING)}</text>')
    out.append(f'<text x="500" y="112" text-anchor="middle" font-family="{SANS}" font-size="58" '
               f'font-weight="800" fill="url(#name)" filter="url(#glow)" letter-spacing="1">{escape(NAME)}</text>')

    # Typewriter tagline: each role is revealed by a stepped clip rect.
    fs, cw, base_y = 22, 13.2, 156
    type_dt, del_dt, hold, pause = 0.07, 0.035, 1.7, 0.35
    t, cursor, plans = 0.4, [(0, 500 - len(ROLES[0]) * cw / 2)], []
    for role in ROLES:
        n, x0 = len(role), 500 - len(role) * cw / 2
        ev = [(0, 0)]
        cursor.append((t, x0))
        for k in range(1, n + 1):
            ev.append((t + k * type_dt, k * cw))
            cursor.append((t + k * type_dt, x0 + k * cw))
        t += n * type_dt + hold
        for k in range(1, n + 1):
            ev.append((t + k * del_dt, (n - k) * cw))
            cursor.append((t + k * del_dt, x0 + (n - k) * cw))
        t += n * del_dt + pause
        plans.append((role, x0, ev))
    total = t
    for i, (role, x0, ev) in enumerate(plans):
        out.append(f'<clipPath id="role{i}"><rect x="{x0:.1f}" y="{base_y - 22}" width="0" height="30">'
                   f'{discrete("width", ev, total)}</rect></clipPath>')
        out.append(f'<text x="{x0:.1f}" y="{base_y}" font-family="{MONO}" font-size="{fs}" fill="#2de2e6" '
                   f'textLength="{len(role) * cw:.1f}" lengthAdjust="spacingAndGlyphs" '
                   f'clip-path="url(#role{i})">{escape(role)}</text>')
    out.append(f'<rect x="{cursor[0][1]:.1f}" y="{base_y - 19}" width="3" height="24" fill="#2de2e6">'
               f'{discrete("x", [(tt, f"{x + 2:.1f}") for tt, x in cursor], total)}'
               f'<animate attributeName="opacity" values="1;0" dur="0.9s" calcMode="discrete" repeatCount="indefinite"/></rect>')

    out.append('</g></svg>')
    return "\n".join(out)


def terminal():
    W, fs, cw, lh, pad = 860, 15, 9.0, 27, 26
    rng = random.Random(42)
    first_y = 76
    n_lines = sum(1 + len(o) for _, o in SESSION) + 1
    H = first_y + (n_lines - 1) * lh + 30
    cmd_x = pad + (len(PROMPT) + 1) * cw

    body, cursor, lines = [], [], []
    t, row = 0.0, 0
    prompt_rows = []
    for cmd, outputs in SESSION:
        y = first_y + row * lh
        prompt_rows.append((t, y))
        cursor.append((t, cmd_x, y))
        t += 0.6
        ev, w = [(0, 0)], 0
        for k in range(1, len(cmd) + 1):
            t += rng.uniform(0.035, 0.11)
            w = k * cw
            ev.append((t, w))
            cursor.append((t, cmd_x + w, y))
        lines.append(("cmd", cmd, y, ev))
        t += 0.45
        row += 1
        for segs in outputs:
            lines.append(("out", segs, first_y + row * lh, t))
            row += 1
            t += 0.15
        t += 0.55
    final_y = first_y + row * lh
    prompt_rows.append((t, final_y))
    cursor.append((t, cmd_x, final_y))
    total = t + 5.0

    for start, y in prompt_rows:
        vis = discrete("opacity", [(0, 0), (start, 1)], total) if start > 0 else ""
        body.append(f'<text x="{pad}" y="{y}" opacity="{0 if start > 0 else 1}" textLength="{len(PROMPT) * cw}" '
                    f'lengthAdjust="spacingAndGlyphs"><tspan fill="#7ee787">abhishek@github</tspan>'
                    f'<tspan fill="#8b949e">:</tspan><tspan fill="#58a6ff">~</tspan><tspan fill="#e6edf3">$</tspan>{vis}</text>')
    for i, line in enumerate(lines):
        if line[0] == "cmd":
            _, cmd, y, ev = line
            body.append(f'<clipPath id="cmd{i}"><rect x="{cmd_x}" y="{y - 18}" width="0" height="26">'
                        f'{discrete("width", ev, total)}</rect></clipPath>')
            body.append(f'<text x="{cmd_x}" y="{y}" fill="#e6edf3" textLength="{len(cmd) * cw}" '
                        f'lengthAdjust="spacingAndGlyphs" clip-path="url(#cmd{i})">{escape(cmd)}</text>')
        else:
            _, segs, y, start = line
            spans = "".join(f'<tspan fill="{c or "#e6edf3"}">{escape(s)}</tspan>' for s, c in segs)
            body.append(f'<text x="{pad}" y="{y}" opacity="0" xml:space="preserve">{spans}'
                        f'{discrete("opacity", [(0, 0), (start, 1)], total)}</text>')
    body.append(f'<g><rect x="{cmd_x}" y="{first_y - 15}" width="{cw}" height="19" fill="#2de2e6" opacity="0.85">'
                f'{discrete("x", [(tt, x) for tt, x, _ in cursor], total)}'
                f'{discrete("y", [(tt, y - 15) for tt, _, y in cursor], total)}</rect>'
                f'<animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/></g>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <linearGradient id="border" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">
    <stop offset="0" stop-color="#ff3cac"/><stop offset="0.5" stop-color="#784ba0"/><stop offset="1" stop-color="#2de2e6"/>
    <animateTransform attributeName="gradientTransform" type="rotate" from="0 {W / 2} {H / 2}" to="360 {W / 2} {H / 2}" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <filter id="soft" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="14" fill="none" stroke="url(#border)" stroke-width="4" filter="url(#soft)" opacity="0.8"/>
<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="14" fill="#0d1117" stroke="url(#border)" stroke-width="1.5"/>
<path d="M4 18 a14 14 0 0 1 14 -14 h{W - 36} a14 14 0 0 1 14 14 v22 h-{W - 8} z" fill="#161b22"/>
<line x1="4" x2="{W - 4}" y1="40" y2="40" stroke="#30363d"/>
<circle cx="28" cy="22" r="6" fill="#ff5f57"/><circle cx="48" cy="22" r="6" fill="#febc2e"/><circle cx="68" cy="22" r="6" fill="#28c840"/>
<text x="{W / 2}" y="27" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#8b949e">abhishek@github: ~ (zsh)</text>
<g font-family="{MONO}" font-size="{fs}">
{chr(10).join(body)}
</g>
</svg>'''


PROJECTS = {
    "homelab": {
        "lines": ["Single-node k3s cluster on a headless laptop,",
                  "reachable only over Tailscale. Provisioned end to",
                  "end with mise, Terraform and 1Password secrets."],
        "tags": [("k3s", "#ffd166"), ("terraform", "#d2a8ff"), ("tailscale", "#2de2e6"), ("aws", "#ff9e64")],
    },
    "email-optimizer": {
        "lines": ["Multi-account email client for bulk spam filtering.",
                  "Connect Gmail over OAuth + IMAP, group by sender,",
                  "block in bulk. Nothing is ever deleted."],
        "tags": [("typescript", "#58a6ff"), ("imap", "#7ee787"), ("oauth", "#ff3cac"), ("sqlite", "#2de2e6")],
    },
}


def box(x, y, w, h, label, color):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#161b22" stroke="{color}" stroke-width="1.5"/>'
            f'<text x="{x + w / 2}" y="{y + h - 9}" text-anchor="middle" font-family="{MONO}" font-size="11" '
            f'fill="{color}">{label}</text>')


def homelab_visual():
    out = [
        '<path d="M95 62 H170 M260 62 H330" stroke="#30363d" stroke-width="2" stroke-dasharray="4 5"/>',
        box(25, 30, 70, 54, "laptop", "#e6edf3"),
        '<rect x="45" y="40" width="30" height="18" rx="2" fill="none" stroke="#e6edf3" stroke-width="1.5"/>'
        '<path d="M40 61 h40" stroke="#e6edf3" stroke-width="1.5"/>',
        box(170, 30, 90, 54, "tailscale", "#2de2e6"),
    ]
    for i in range(3):
        for j in range(3):
            out.append(f'<circle cx="{203 + j * 12}" cy="{41 + i * 7}" r="2" fill="#2de2e6" opacity="{0.4 if (i + j) % 2 else 1}"/>')
    out.append(box(330, 22, 80, 70, "k3s", "#ffd166"))
    for k in range(6):
        x, y = 345 + (k % 3) * 18, 32 + (k // 3) * 16
        out.append(f'<rect x="{x}" y="{y}" width="12" height="11" rx="2" fill="#7ee787">'
                   f'<animate attributeName="opacity" values="1;0.25;1" dur="{1.6 + k * 0.37:.2f}s" repeatCount="indefinite"/></rect>')
    # Packets hop laptop -> tailscale -> k3s.
    for begin in (0, 0.8, 1.6):
        out.append(f'<circle r="3.5" fill="#ff3cac" opacity="0">'
                   f'<animateMotion path="M95 62 H330" dur="2.4s" begin="{begin}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.05;0.4;0.95;1" dur="2.4s" begin="{begin}s" repeatCount="indefinite"/></circle>')
    out.append('<text x="132" y="52" text-anchor="middle" font-family="' + MONO + '" font-size="9" fill="#8b949e">ssh</text>'
               '<text x="295" y="52" text-anchor="middle" font-family="' + MONO + '" font-size="9" fill="#8b949e">kubectl</text>')
    return "\n".join(out)


def envelope(color):
    return (f'<rect x="-10" y="-7" width="20" height="14" rx="2" fill="#161b22" stroke="{color}" stroke-width="1.5"/>'
            f'<path d="M-10 -6 L0 2 L10 -6" fill="none" stroke="{color}" stroke-width="1.5"/>')


def email_visual():
    out = [
        '<path d="M70 58 H200 M230 58 C270 58 290 34 330 34 M230 58 C270 58 290 84 330 84" fill="none" stroke="#30363d" stroke-width="2" stroke-dasharray="4 5"/>',
        box(18, 24, 52, 70, "gmail", "#e6edf3"),
    ]
    for i in range(3):
        out.append(f'<rect x="30" y="{32 + i * 13}" width="28" height="9" rx="2" fill="none" stroke="#8b949e"/>')
    out.append('<path d="M196 40 H236 L222 62 V76 L210 70 V62 Z" fill="#161b22" stroke="#d2a8ff" stroke-width="1.5"/>'
               f'<text x="216" y="96" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#d2a8ff">group by sender</text>')
    out.append(box(330, 12, 80, 42, "inbox", "#7ee787"))
    out.append(box(330, 64, 80, 42, "blocked", "#ff7b72"))
    # Mail flows into the filter, then wanted mail goes up and bulk mail goes down.
    for i, (dest, color) in enumerate([("M216 58 C270 58 290 34 360 30", "#7ee787"),
                                       ("M216 58 C270 58 290 84 360 82", "#ff7b72"),
                                       ("M216 58 C270 58 290 84 360 82", "#ff7b72")]):
        begin = i * 1.1
        path = "M70 58 H216 " + dest[len("M216 58 "):]
        out.append(f'<g opacity="0">{envelope(color)}'
                   f'<animateMotion path="{path}" dur="3.3s" begin="{begin}s" repeatCount="indefinite" '
                   f'keyPoints="0;0.45;1" keyTimes="0;0.5;1" calcMode="linear"/>'
                   f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.88;1" dur="3.3s" begin="{begin}s" repeatCount="indefinite"/></g>')
    return "\n".join(out)


def project_card(name, project, visual):
    W, H = 430, 266
    lines = "".join(f'<text x="24" y="{164 + i * 19}" font-family="{SANS}" font-size="13" fill="#8b949e">{escape(line)}</text>'
                    for i, line in enumerate(project["lines"]))
    tags, x = [], 24
    for label, color in project["tags"]:
        w = len(label) * 6.6 + 18
        tags.append(f'<rect x="{x}" y="{H - 40}" width="{w:.1f}" height="22" rx="11" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.5"/>'
                    f'<text x="{x + 9}" y="{H - 25}" font-family="{MONO}" font-size="11" fill="{color}" '
                    f'textLength="{len(label) * 6.6:.1f}" lengthAdjust="spacingAndGlyphs">{escape(label)}</text>')
        x += w + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <linearGradient id="border" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">
    <stop offset="0" stop-color="#ff3cac"/><stop offset="0.5" stop-color="#784ba0"/><stop offset="1" stop-color="#2de2e6"/>
    <animateTransform attributeName="gradientTransform" type="rotate" from="0 {W / 2} {H / 2}" to="360 {W / 2} {H / 2}" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ff3cac"/><stop offset="1" stop-color="#2de2e6"/>
  </linearGradient>
</defs>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="14" fill="#0d1117" stroke="url(#border)" stroke-width="1.5"/>
<g transform="translate(0 6)">
{visual}
</g>
<text x="24" y="138" font-family="{SANS}" font-size="20" font-weight="700" fill="url(#title)">{escape(name)}</text>
<text x="{W - 24}" y="138" text-anchor="end" font-family="{MONO}" font-size="11" fill="#8b949e">view repo -&gt;</text>
{lines}
{"".join(tags)}
</svg>'''


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    outputs = {
        "header.svg": header(),
        "terminal.svg": terminal(),
        "project-homelab.svg": project_card("homelab", PROJECTS["homelab"], homelab_visual()),
        "project-email-optimizer.svg": project_card("email-optimizer", PROJECTS["email-optimizer"], email_visual()),
    }
    for filename, svg in outputs.items():
        (ASSETS / filename).write_text(svg + "\n")
        print(f"wrote {ASSETS / filename}")
