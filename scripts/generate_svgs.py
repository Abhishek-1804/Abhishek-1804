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
    "Software Developer",
    "Data Scientist",
    "Python Enthusiast",
    "Building scalable things",
]

PROMPT = "abhishek@github:~$"
# Each entry is a typed command followed by its output lines; an output line is
# a list of (text, color) segments.
SESSION = [
    ("whoami", [
        [("Abhishek Deshpande", "#e6edf3"), (" // software developer & data scientist", "#8b949e")],
    ]),
    ("cat currently_learning.txt", [
        [("[next.js]", "#e6edf3"), ("  ", ""), ("[kubernetes]", "#58a6ff"), ("  ", ""),
         ("[docker]", "#2de2e6"), ("  ", ""), ("[ci/cd]", "#f778ba"), ("  ", ""), ("[linux]", "#ffd166")],
    ]),
    ("node -e \"console.log([] == ![])\"", [
        [("true", "#7ee787")],
        [("// equal isn't always equal in JavaScript", "#8b949e")],
    ]),
    ("open https://abhishekdp.com", [
        [("-> launching portfolio", "#d2a8ff"), (" ...", "#8b949e")],
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


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "header.svg").write_text(header() + "\n")
    (ASSETS / "terminal.svg").write_text(terminal() + "\n")
    print(f"wrote {ASSETS / 'header.svg'} and {ASSETS / 'terminal.svg'}")
