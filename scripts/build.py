"""Draws the images in assets/ and updates the date in README.md.

Contribution counts come from the public contribution graph, so the numbers match what visitors see.
Standard library only. Run from the repo root: python3 scripts/build.py
"""
import base64, datetime as dt, json, math, re, urllib.request
from pathlib import Path

USER = 'RajaATAli'
FIRST_YEAR = 2021
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'assets'
ICONS = json.loads((ROOT / 'scripts/icons.json').read_text())
FONT = base64.b64encode((ROOT / 'scripts/JetBrainsMono-Medium.woff').read_bytes()).decode()

PAL = {
    'dark':  dict(bg='#16323F', tile='#1B3A48', fg='#F4EFE3', mute='#D9D2C0', ring='rgba(244,239,227,.22)', dot='rgba(244,239,227,.07)',
                  acc='#C8842A', acc_text='#E8A951', w1='#8C6630', w2='#C8842A', w3='#F2C27A',
                  ecg1='rgba(200,132,42,.10)', ecg2='rgba(200,132,42,.22)', dim='rgba(244,239,227,.30)'),
    'light': dict(bg='#F4EFE3', tile='#EBE3D0', fg='#16323F', mute='#3A332E', ring='#C7BEA9', dot='rgba(22,50,63,.08)',
                  acc='#C8842A', acc_text='#8A5616', w1='#E0B97F', w2='#C8842A', w3='#8A5616',
                  ecg1='rgba(200,132,42,.14)', ecg2='rgba(200,132,42,.30)', dim='rgba(22,50,63,.28)'),
}
STILL = '@media (prefers-reduced-motion:reduce){.anim{display:none}}'


def fetch_contributions():
    days = {}
    for year in range(FIRST_YEAR, dt.date.today().year + 1):
        url = f'https://github.com/users/{USER}/contributions?from={year}-01-01&to={year}-12-31'
        req = urllib.request.Request(url, headers={'User-Agent': 'profile-readme-build'})
        html = urllib.request.urlopen(req, timeout=30).read().decode()
        cells = {cid: date for date, cid in re.findall(r'data-date="([0-9-]+)" id="([^"]+)"', html)}
        tips = dict(re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)<', html))
        if len(cells) < 365:
            raise SystemExit(f'Could not read the contribution graph for {year}; GitHub may have changed the page.')
        for cid, date in cells.items():
            m = re.match(r'(\d+) contribution', tips.get(cid, ''))
            days[date] = int(m.group(1)) if m else 0
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    return {k: v for k, v in sorted(days.items()) if k <= today}


def svg(w, h, body, css, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">'
            f"<style>@font-face{{font-family:'JBM';src:url(data:font/woff;base64,{FONT}) format('woff')}}"
            f'text{{font-family:JBM,ui-monospace,monospace;font-weight:500}}{css}</style>{body}</svg>')


def ground(w, h, p):
    return (f'<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="1" fill="{p["dot"]}"/></pattern></defs>'
            f'<rect width="{w}" height="{h}" fill="{p["bg"]}"/><rect width="{w}" height="{h}" fill="url(#g)"/>')


def long_date(d):
    return d.strftime('%-d %b %Y').upper()


# Header: five areas of work, with a signal passing through them in turn.
THESIS = [('ai', 'AI / ML'), ('systems', 'SYSTEMS'), ('dna', 'LIFE SCIENCES'), ('molecule', 'DRUG DISCOVERY'), ('health', 'HEALTHCARE')]

def hero(p):
    W, H = 1000, 420
    X0, STEP, TOP, BOT, R = 112, 194, 238, 334, 40
    nodes = [(X0 + i * STEP, TOP if i % 2 == 0 else BOT) for i in range(5)]
    css = f"""
      .fig{{stroke:{p['fg']};stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}}
      .fig .solid,.fig .dot{{fill:{p['fg']};stroke:none}} .fig .on{{fill:{p['acc_text']};stroke:none}}
      .fig .cold{{stroke:{p['fg']};stroke-opacity:.35;stroke-width:1}} .fig .hot{{stroke:{p['acc_text']};stroke-width:1.8}}
      .fig .off{{fill:{p['bg']};stroke:{p['fg']};stroke-width:1.6}} .fig .halo{{fill:none;stroke:{p['acc_text']};stroke-opacity:.45;stroke-width:1.2}}
      .edge{{stroke:{p['ring']};stroke-width:1}} .edge.t{{stroke:{p['acc']};stroke-width:1.6}}
      .ring{{fill:{p['bg']};stroke:{p['acc']};stroke-opacity:.8;stroke-width:1.2}}
      .cap{{font-size:15px;letter-spacing:.1em;fill:{p['mute']}}}
      .h1{{font-size:24px;letter-spacing:.18em;fill:{p['fg']}}} .h2{{font-size:18px;letter-spacing:.04em;fill:{p['acc_text']}}}
      .h3{{font-size:18px;letter-spacing:.04em;fill:{p['fg']};opacity:.85}}
      .sig{{fill:none;stroke:{p['acc_text']};stroke-width:3;stroke-linecap:round;stroke-dasharray:40 2000;stroke-dashoffset:40;opacity:0}}
      @media (prefers-reduced-motion:no-preference){{
        .sig{{animation:pass 6s cubic-bezier(.45,0,.55,1) infinite}}
        @keyframes pass{{0%{{stroke-dashoffset:40;opacity:1}}72%{{stroke-dashoffset:-880;opacity:1}}73%,100%{{opacity:0;stroke-dashoffset:-880}}}}
        .ring{{animation:lit 6s infinite}} {''.join(f'.r{i}{{animation-delay:{i*1.04:.2f}s}}' for i in range(5))}
        @keyframes lit{{0%,100%{{stroke-width:1.2;stroke-opacity:.8}}4%{{stroke-width:3.4;stroke-opacity:1}}16%{{stroke-width:1.2;stroke-opacity:.8}}}}
      }}"""
    b = [ground(W, H, p),
         '<text x="48" y="62" class="h1">RAJA ALI</text>',
         '<text x="48" y="98" class="h2">AI/ML INFRA · DISTRIBUTED SYSTEMS</text>',
         '<text x="48" y="124" class="h3">FOR LIFE SCIENCES, BIOPHARMA &amp; HEALTHCARE</text>']
    hot = {(0, 1), (1, 2), (0, 2), (2, 3), (3, 4)}
    for i in range(5):
        for j in (i + 1, i + 2):
            if j < 5:
                (x1, y1), (x2, y2) = nodes[i], nodes[j]
                b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="edge{" t" if (i, j) in hot else ""}"/>')
    b.append('<path d="M' + ' L'.join(f'{x} {y}' for x, y in nodes) + '" class="sig"/>')
    for i, ((x, y), (key, label)) in enumerate(zip(nodes, THESIS)):
        s = 0.9
        b.append(f'<circle cx="{x}" cy="{y}" r="{R}" class="ring r{i}"/>'
                 f'<g class="fig" transform="translate({x-32*s} {y-32*s}) scale({s})">{ICONS["figures"][key]}</g>')
        ty = y - R - 16 if y == TOP else y + R + 28
        b.append(f'<text x="{x}" y="{ty}" text-anchor="middle" class="cap">{label}</text>')
    return svg(W, H, ''.join(b), css, 'Raja Ali: AI/ML infra and distributed systems for life sciences, biopharma and healthcare')


# Link icons: one file for both themes. LinkedIn is the one in saffron.
def link_tile(name):
    color = '#E8A951' if name == 'linkedin' else '#F4EFE3'
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">'
            '<rect width="48" height="48" fill="#16323F"/><rect x=".5" y=".5" width="47" height="47" fill="none" stroke="rgba(244,239,227,.18)"/>'
            f'<g transform="translate(11 11) scale(.1016)" style="color:{color}">{ICONS["links"][name]}</g></svg>')


def streaks(days, keys):
    end = len(keys) - 1
    if days[keys[end]] == 0:          # today still counts until it's over
        end -= 1
    current, k = 0, end
    while k >= 0 and days[keys[k]] > 0:
        current += 1
        k -= 1
    best, run, start, span = 0, 0, None, None
    for key in keys:
        if days[key] > 0:
            run += 1
            start = start or key
            if run > best:
                best, span = run, (start, key)
        else:
            run, start = 0, None
    return current, keys[end - current + 1:end + 1], best, span


def heartbeat(x, w, h):
    a = w / 20
    return (f' L{x+3*a:.1f} 0 Q{x+4.5*a:.1f} {-h*.12:.1f} {x+6*a:.1f} 0 L{x+8*a:.1f} 0 L{x+9*a:.1f} {h*.16:.1f}'
            f' L{x+10*a:.1f} {-h:.1f} L{x+11*a:.1f} {h*.30:.1f} L{x+12*a:.1f} 0 L{x+13.5*a:.1f} 0'
            f' Q{x+15.5*a:.1f} {-h*.22:.1f} {x+17.5*a:.1f} 0 L{x+w:.1f} 0')


def peak_height(count):
    return min(92, 20 + 24 * math.log2(1 + count))


# Streak: a heart monitor of the last 30 days.
def monitor(p, days):
    keys = list(days)
    W, H = 1000, 300
    current, run_days, best, _ = streaks(days, keys)
    run_days = set(run_days)
    total = sum(days.values())
    since = next(k for k in keys if days[k])[:4]
    last = keys[-30:]
    TX, TW, BASE = 372, 580, 168
    cw = TW / len(last)
    trace, lit, ping = f'M{TX} 0', [], None
    for i, key in enumerate(last):
        x0 = TX + i * cw
        seg = heartbeat(x0, cw, peak_height(days[key])) if days[key] else f' L{x0+cw:.1f} 0'
        trace += seg
        if key in run_days:
            lit.append(f'M{x0:.1f} 0' + seg)
            ping = (x0 + cw / 2, -peak_height(days[key]))
    css = f"""
      .k{{font-size:14px;letter-spacing:.14em;fill:{p['mute']};opacity:.85}} .ax{{font-size:13px;letter-spacing:.06em;fill:{p['mute']};opacity:.7}}
      .big{{font-size:132px;fill:{p['acc_text']};letter-spacing:-.04em}} .unit{{font-size:20px;letter-spacing:.12em;fill:{p['fg']}}}
      .tot{{font-size:15px;letter-spacing:.06em;fill:{p['fg']};opacity:.85}}
      .g1{{stroke:{p['ecg1']};stroke-width:1}} .g2{{stroke:{p['ecg2']};stroke-width:1}}
      .tr{{fill:none;stroke:{p['dim']};stroke-width:1.8;stroke-linejoin:round}}
      .now{{fill:none;stroke:{p['acc_text']};stroke-width:2.4;stroke-linejoin:round}}
      .draw{{fill:none;stroke:{p['acc_text']};stroke-width:2.4;stroke-linejoin:round;stroke-dasharray:1000;stroke-dashoffset:1000}}
      .head{{fill:{p['acc_text']}}} .seg{{fill:none;stroke:{p['ring']};stroke-width:1}} .seg.on{{fill:{p['acc_text']};stroke:none}}
      .beat{{fill:{p['acc_text']}}} .ping{{fill:none;stroke:{p['acc_text']};stroke-width:1.6;opacity:0;transform-box:fill-box;transform-origin:center}}
      @media (prefers-reduced-motion:no-preference){{
        .draw{{animation:draw 5s linear infinite}} @keyframes draw{{0%{{stroke-dashoffset:1000;opacity:1}}88%{{stroke-dashoffset:0;opacity:1}}100%{{stroke-dashoffset:0;opacity:0}}}}
        .beat{{animation:beat 1s ease-out infinite;transform-origin:56px 82px}} @keyframes beat{{0%{{transform:scale(1)}}12%{{transform:scale(1.7)}}30%,100%{{transform:scale(1)}}}}
        .ping{{animation:ping 1.2s ease-out infinite}} @keyframes ping{{0%{{transform:scale(1);opacity:.9}}100%{{transform:scale(4.5);opacity:0}}}}
        .seg.on{{animation:glow 2.4s ease-in-out infinite}} @keyframes glow{{50%{{opacity:.55}}}}
      }} {STILL}"""
    b = [f'<rect width="{W}" height="{H}" fill="{p["bg"]}"/>']
    gx0, gy0, gx1, gy1 = TX - 10, 50, TX + TW + 10, 250
    for x in range(gx0, gx1 + 1, 10):
        b.append(f'<line x1="{x}" y1="{gy0}" x2="{x}" y2="{gy1}" class="{"g2" if (x - gx0) % 50 == 0 else "g1"}"/>')
    for y in range(gy0, gy1 + 1, 10):
        b.append(f'<line x1="{gx0}" y1="{y}" x2="{gx1}" y2="{y}" class="{"g2" if (y - gy0) % 50 == 0 else "g1"}"/>')
    b.append('<circle cx="56" cy="82" r="5" class="beat"/><text x="72" y="87" class="k">CURRENT STREAK</text>')
    b.append(f'<text x="40" y="208" class="big">{current}</text>')
    b.append(f'<text x="{48 + 80 * len(str(current)) + 8}" y="206" class="unit">{"DAY" if current == 1 else "DAYS"}</text>')
    cells = max(best, current, 1)
    sw = min(18, 228 / cells)
    for i in range(cells):
        b.append(f'<rect x="{48 + i*sw:.1f}" y="234" width="{sw-4:.1f}" height="10" class="seg{" on" if i < current else ""}"/>')
    record = 'NEW RECORD' if current and current >= best else f'RECORD {best} · {best - current} TO BEAT IT'
    b.append(f'<text x="48" y="268" class="ax">{record}</text>')
    b.append(f'<text x="{TX+TW}" y="34" text-anchor="end" class="tot">{total:,} CONTRIBUTIONS SINCE {since}</text>')
    t = f'translate(0 {BASE})'
    b.append(f'<path id="tr" d="{trace}" class="tr" transform="{t}"/>')
    b += [f'<path d="{d}" class="now" transform="{t}"/>' for d in lit]
    if ping:
        px, py = ping
        b.append(f'<g transform="{t}" class="anim">'
                 + ''.join(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" class="ping" style="animation-delay:{k*.6}s"/>' for k in range(2))
                 + f'</g><circle cx="{px:.1f}" cy="{py:.1f}" r="4" class="head" transform="{t}"/>')
    b.append(f'<path d="{trace}" class="draw anim" pathLength="1000" transform="{t}"/>')
    b.append(f'<g transform="{t}" class="anim"><circle r="4.5" class="head"><animateMotion dur="5s" repeatCount="indefinite" '
             'keyPoints="0;1;1" keyTimes="0;.88;1" calcMode="linear"><mpath href="#tr"/></animateMotion></circle></g>')
    short = lambda k: dt.date.fromisoformat(k).strftime('%-d %b').upper()
    b.append(f'<text x="{TX}" y="276" class="ax">{short(last[0])}</text>'
             f'<text x="{TX+TW/2}" y="276" text-anchor="middle" class="ax">LAST 30 DAYS</text>'
             f'<text x="{TX+TW}" y="276" text-anchor="end" class="ax">TODAY</text>')
    return svg(W, H, ''.join(b), css, f'Current streak: {current} days. Longest: {best}.')


# Contribution grid: one circle per day for the last 384 days, laid out like a 384-well plate.
def plate(p, days):
    keys = list(days)[-384:]
    v = [days[k] for k in keys]
    start, end = dt.date.fromisoformat(keys[0]), dt.date.fromisoformat(keys[-1])
    total, peak = sum(v), max(v)
    peak_at = v.index(peak)
    W, H = 1000, 600
    PX, PY, PITCH, COLS, ROWS = 92, 100, 28, 24, 16
    css = f"""
      .h3{{font-size:15px;letter-spacing:.06em;fill:{p['mute']};opacity:.85}} .n{{fill:{p['acc_text']}}}
      .ax{{font-size:12px;letter-spacing:.04em;fill:{p['mute']};opacity:.7}}
      .k{{font-size:13px;letter-spacing:.12em;fill:{p['mute']};opacity:.8}} .val{{font-size:30px;fill:{p['fg']}}}
      .plate{{fill:none;stroke:{p['ring']};stroke-width:1.2}} .e{{fill:none;stroke:{p['ring']};stroke-width:1}}
      .w1{{fill:{p['w1']}}} .w2{{fill:{p['w2']}}} .w3{{fill:{p['w3']}}}
      .pk{{stroke:{p['acc_text']};stroke-width:1;fill:none}} .today{{fill:none;stroke:{p['acc_text']};stroke-width:1.4}}
      @media (prefers-reduced-motion:no-preference){{.today{{animation:blink 2s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}}}"""
    b = [ground(W, H, p), f'<text x="48" y="44" class="h3">{long_date(start)} → {long_date(end)}</text>']
    x0, y0, x1, y1 = PX - 34, PY - 34, PX + COLS * PITCH + 6, PY + ROWS * PITCH + 6
    b.append(f'<path d="M{x0+16} {y0} H{x1} V{y1} H{x0} V{y0+16} Z" class="plate"/>')
    b += [f'<text x="{PX + c*PITCH + 14}" y="{PY - 12}" text-anchor="middle" class="ax">{c+1}</text>' for c in range(COLS)]
    b += [f'<text x="{PX - 14}" y="{PY + r*PITCH + 18}" text-anchor="middle" class="ax">{chr(65+r)}</text>' for r in range(ROWS)]
    for i, count in enumerate(v):
        r, c = divmod(i, COLS)
        cx, cy = PX + c * PITCH + 14, PY + r * PITCH + 14
        cls = 'e' if count == 0 else 'w1' if count <= 2 else 'w2' if count <= 9 else 'w3'
        b.append(f'<circle cx="{cx}" cy="{cy}" r="10" class="{cls}"/>')
        if i == len(v) - 1:
            b.append(f'<rect x="{cx-14}" y="{cy-14}" width="28" height="28" class="today"/>')
        if i == peak_at:
            b.append(f'<circle cx="{cx}" cy="{cy}" r="13.5" class="pk"/>')
    rx = 800
    b.append(f'<text x="{rx}" y="{PY+4}" class="k">CONTRIBUTIONS</text><text x="{rx}" y="{PY+42}" class="val">{total:,}</text>')
    b.append(f'<text x="{rx}" y="{PY+96}" class="k">PEAK DAY</text><text x="{rx}" y="{PY+134}" class="val">{peak}</text>')
    b.append(f'<text x="{rx}" y="{PY+158}" class="ax">{long_date(start + dt.timedelta(days=peak_at))}</text>')
    for k, (cls, label) in enumerate([('e', '0'), ('w1', '1–2'), ('w2', '3–9'), ('w3', '10+')]):
        b.append(f'<circle cx="{rx+9}" cy="{PY+352+k*26}" r="8" class="{cls}"/><text x="{rx+26}" y="{PY+357+k*26}" class="ax">{label}</text>')
    b.append(f'<text x="48" y="{H-28}" class="h3"><tspan class="n">†</tspan> most of the real work lives in a private repo.</text>')
    return svg(W, H, ''.join(b), css, f'{total} contributions from {long_date(start)} to {long_date(end)}, one circle per day')


# Tools, laid out as a periodic table. (icon key, label); None is the empty "next" cell.
GROUPS = [
    ('LANGUAGES', 3, [('python', 'python'), ('typescript', 'typescript'), ('javascript', 'javascript'), ('openjdk', 'java'), ('c', 'c'),
                      ('cplusplus', 'c++'), ('r', 'r'), ('matlab', 'matlab'), ('fortran', 'fortran')]),
    ('BUILD &amp; DATA', 3, [('fastapi', 'fastapi'), ('django', 'django'), ('nodedotjs', 'node'), ('react', 'react'), ('graphql', 'graphql'),
                             ('postgresql', 'postgres'), ('redis', 'redis'), ('microsoftsqlserver', 'sql server'), ('unity', 'unity')]),
    ('ML &amp; ANALYTICS', 2, [('tensorflow', 'tensorflow'), ('mlflow', 'mlflow'), ('openai', 'openai'), ('databricks', 'databricks'),
                               ('powerbi', 'power bi'), (None, 'next')]),
    ('INFRA', 2, [('amazonwebservices', 'aws'), ('docker', 'docker'), ('terraform', 'terraform'), ('linux', 'linux'), ('git', 'git'), ('gnubash', 'bash')]),
]

def stack(p):
    W = 1000
    TW, TH, GAP, X0, Y0 = 86, 96, 8, 48, 92
    H = Y0 + 3 * (TH + GAP) + 40
    css = f"""
      .t{{fill:{p['tile']};stroke:{p['ring']};stroke-width:1}} .t.q{{fill:none;stroke-dasharray:4 4}}
      .num{{font-size:12px;fill:{p['mute']};opacity:.75}} .nm{{font-size:12px;fill:{p['fg']};opacity:.9}}
      .lg{{color:{p['fg']}}} .qm{{font-size:30px;fill:{p['acc_text']}}}
      .gl{{font-size:14px;letter-spacing:.12em;fill:{p['acc_text']}}} .brace{{fill:none;stroke:{p['acc']};stroke-width:1.2}}
      @media (prefers-reduced-motion:no-preference){{
        .t{{animation:exc 9s infinite}} .num{{animation:excn 9s infinite}}
        @keyframes exc{{0%,100%{{stroke:{p['ring']};stroke-width:1}}3%{{stroke:{p['acc_text']};stroke-width:2.4}}9%{{stroke:{p['ring']};stroke-width:1}}}}
        @keyframes excn{{0%,100%{{fill:{p['mute']}}}3%{{fill:{p['acc_text']}}}9%{{fill:{p['mute']}}}}}
        {''.join(f'.c{c}{{animation-delay:{c*0.14:.2f}s}}' for c in range(10))}
      }}"""
    b = [ground(W, H, p)]
    col, z = 0, 1
    for name, ncols, items in GROUPS:
        gx0 = X0 + col * (TW + GAP)
        gx1 = gx0 + ncols * (TW + GAP) - GAP
        b.append(f'<path d="M{gx0} {Y0-14} V{Y0-22} H{gx1} V{Y0-14}" class="brace"/><text x="{gx0}" y="{Y0-34}" class="gl">{name}</text>')
        for k, (icon, label) in enumerate(items):
            r, c = divmod(k, ncols)
            x, y, cc = X0 + (col + c) * (TW + GAP), Y0 + r * (TH + GAP), col + c
            if icon is None:
                b.append(f'<rect x="{x}" y="{y}" width="{TW}" height="{TH}" class="t q"/><text x="{x+TW/2}" y="{y+56}" text-anchor="middle" class="qm">?</text>'
                         f'<text x="{x+TW/2}" y="{y+TH-12}" text-anchor="middle" class="nm">{label}</text>')
                continue
            glyph = ICONS['tools'][icon]
            b.append(f'<rect x="{x}" y="{y}" width="{TW}" height="{TH}" class="t c{cc}"/><text x="{x+8}" y="{y+18}" class="num c{cc}">{z}</text>'
                     f'<g class="lg" transform="translate({x+TW/2-15} {y+24}) scale({30 / glyph["size"]:.4f})">{glyph["body"]}</g>'
                     f'<text x="{x+TW/2}" y="{y+TH-12}" text-anchor="middle" class="nm">{label}</text>')
            z += 1
        col += ncols
    return svg(W, H, ''.join(b), css, 'Languages, tools and technologies')


def main():
    days = fetch_contributions()
    ASSETS.mkdir(exist_ok=True)
    for mode, p in PAL.items():
        (ASSETS / f'hero-{mode}.svg').write_text(hero(p))
        (ASSETS / f'streak-{mode}.svg').write_text(monitor(p, days))
        (ASSETS / f'plate-{mode}.svg').write_text(plate(p, days))
        (ASSETS / f'stack-{mode}.svg').write_text(stack(p))
    for name in ICONS['links']:
        (ASSETS / f'link-{name}.svg').write_text(link_tile(name))
    readme = ROOT / 'README.md'
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%-d %b %Y').lower()
    readme.write_text(re.sub(r'<!--date-->.*?<!--/date-->', f'<!--date-->{stamp}<!--/date-->', readme.read_text()))


if __name__ == '__main__':
    main()
