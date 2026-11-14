#!/usr/bin/env python3
"""Builds the static, animated SVG assets (hero, headings, case cards, mind palace, footer)."""
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

C = dict(
    SANS="'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif",
    MONO="'Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace",
    BG="#0b1018", BG2="#121a2c", PANEL="#0e1524", LINE="#1f2a3d",
    VIOLET="#8b7cff", TEAL="#2dd4bf", AMBER="#f59e0b", TEXT="#e6edf7", MUTED="#9fb0c8",
)


def tpl(s, **kw):
    for k, v in {**C, **kw}.items():
        s = s.replace(f"%{k}%", str(v))
    return s


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def save(name, svg):
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", name)


# ───────────────────────── HERO ─────────────────────────
HERO = """
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="340" viewBox="0 0 900 340" role="img" aria-label="Aviral Mishra: competitive programmer and full-stack developer">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%BG%"/><stop offset="1" stop-color="%BG2%"/></linearGradient>
  <linearGradient id="nm" x1="0" x2="1"><stop offset="0" stop-color="%VIOLET%"/><stop offset="1" stop-color="%TEAL%"/></linearGradient>
  <radialGradient id="bob" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#fde68a"/><stop offset="1" stop-color="#b45309"/></radialGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="%AMBER%" stop-opacity=".55"/><stop offset="1" stop-color="%AMBER%" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#ffffff" stroke-opacity=".035"/></pattern>
  __CLIPS__
</defs>
<style>
.tw{opacity:.15;animation:tw 3.4s ease-in-out infinite}
@keyframes tw{50%{opacity:.9}}
.fu{opacity:0;animation:fu .9s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes fu{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.lab{font:600 12px %MONO%;letter-spacing:3px;fill:%AMBER%}
.nm{font:800 60px %SANS%;letter-spacing:-1.5px;fill:url(#nm)}
.sub{font:500 19px %SANS%;fill:%MUTED%}
.chip{font:600 12.5px %SANS%;fill:%TEXT%}
.mono{font:500 13px %MONO%;fill:%MUTED%}
.ln{font:500 15px %MONO%;fill:%TEXT%}
.cur{animation:blink 1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.steam{fill:none;stroke:#cfe3ff;stroke-width:2;stroke-linecap:round;stroke-dasharray:30;opacity:0;animation:steam 3.2s ease-in-out infinite}
@keyframes steam{0%{stroke-dashoffset:30;opacity:0}40%{opacity:.7}100%{stroke-dashoffset:-30;opacity:0}}
.pulse{animation:pulse 1.8s ease-in-out infinite}
@keyframes pulse{50%{opacity:.25}}
.glow{animation:glow 3.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes glow{50%{transform:scale(1.25);opacity:.6}}
</style>

<rect width="900" height="340" rx="18" fill="url(#bg)"/>
<rect width="900" height="340" rx="18" fill="url(#grid)"/>
__STARS__

<!-- label, name, subtitle, chips -->
<g class="fu" style="animation-delay:.1s"><circle class="pulse" cx="52" cy="56" r="4" fill="%AMBER%"/><text class="lab" x="64" y="60">CASE FILE 001 · SUBJECT PROFILE</text></g>
<text class="nm fu" x="46" y="122" style="animation-delay:.25s">Aviral Mishra</text>
<text class="sub fu" x="48" y="154" style="animation-delay:.45s">Competitive programmer  ·  Full-stack developer</text>
__CHIPS__

<!-- cold-reading terminal -->
<g class="fu" style="animation-delay:.9s">
  <rect x="48.5" y="214.5" width="580" height="94" rx="10" fill="%PANEL%" stroke="%LINE%"/>
  <circle cx="68" cy="228" r="4" fill="#ef4444"/><circle cx="83" cy="228" r="4" fill="%AMBER%"/><circle cx="98" cy="228" r="4" fill="#22c55e"/>
  <text class="mono" x="116" y="232" font-size="11">cold_reading.sh</text>
  <text class="mono" x="66" y="258"><tspan fill="%AMBER%">$</tspan> observe --visitor</text>
  <text class="mono" x="66" y="284" style="fill:%AMBER%">&gt;</text>
  __TEXTS__
  __CURSORS__
</g>

<!-- hypnotist's pendulum -->
<path d="M723 154 A140 140 0 0 0 837 154" fill="none" stroke="%LINE%" stroke-dasharray="3 5"/>
<rect x="752" y="18" width="56" height="8" rx="4" fill="#26324a"/>
<g>
  <animateTransform attributeName="transform" type="rotate" values="24 780 26;-24 780 26;24 780 26" keyTimes="0;.5;1" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" dur="3.6s" repeatCount="indefinite"/>
  <line x1="780" y1="26" x2="780" y2="166" stroke="#6b7a99" stroke-width="1.5"/>
  <circle class="glow" cx="780" cy="166" r="34" fill="url(#glow)"/>
  <circle cx="780" cy="166" r="14" fill="url(#bob)" stroke="#fcd34d" stroke-opacity=".6"/>
  <circle cx="780" cy="166" r="7" fill="none" stroke="#7c2d12" stroke-opacity=".5"/>
</g>
<circle cx="780" cy="26" r="4" fill="%MUTED%"/>

<!-- cup of tea -->
<ellipse cx="780" cy="292" rx="44" ry="6" fill="#1a2438"/>
<path d="M808 254 H816 A9 9 0 0 1 816 272 H805" fill="none" stroke="%TEAL%" stroke-opacity=".7" stroke-width="1.5"/>
<path d="M752 248 H808 V262 A28 24 0 0 1 752 262 Z" fill="#16203a" stroke="%TEAL%" stroke-opacity=".7" stroke-width="1.5"/>
<ellipse cx="780" cy="248" rx="28" ry="4" fill="#6b3a12"/>
<path class="steam" style="animation-delay:0s" d="M770 238 q-5 -7 0 -14 t0 -14"/>
<path class="steam" style="animation-delay:1s" d="M780 238 q-5 -7 0 -14 t0 -14"/>
<path class="steam" style="animation-delay:2s" d="M790 238 q-5 -7 0 -14 t0 -14"/>
</svg>
"""


def hero():
    rnd = random.Random(11)
    stars = "".join(
        f'<circle class="tw" cx="{rnd.randint(24, 690)}" cy="{rnd.randint(14, 200)}" r="{rnd.choice([1, 1.2, 1.5])}" '
        f'fill="#cfe3ff" style="animation-delay:{rnd.uniform(0, 4):.2f}s"/>'
        for _ in range(26)
    )
    lines = [
        "You scrolled past the banner first. Visual thinker.",
        "Checking whether these projects are real? They are.",
        "You will click a link within ten seconds. Go ahead.",
    ]
    n = len(lines)
    seg = 1 / n
    char = 9
    clips, texts, cursors = [], [], []
    for i, s in enumerate(lines):
        k = len(s)
        a = i * seg
        # keyTimes for the reveal width (discrete = typewriter steps)
        kt = [0.0] + [a + 0.12 * j / k for j in range(1, k + 1)] + [a + 0.31, 1.0]
        vals = [0] + [char * j for j in range(1, k + 1)] + [0, 0]
        kt_s = ";".join(f"{t:.4f}" for t in kt)
        clips.append(
            f'<clipPath id="r{i}"><rect x="84" y="262" width="0" height="34">'
            f'<animate attributeName="width" dur="20s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt_s}" values="{";".join(map(str, vals))}"/>'
            f"</rect></clipPath>"
        )
        texts.append(
            f'<text class="ln" x="84" y="284" textLength="{k * char}" lengthAdjust="spacing" clip-path="url(#r{i})">{esc(s)}</text>'
        )
        xs = [84] + [84 + char * j for j in range(1, k + 1)] + [84, 84]
        if a == 0:
            op_kt, op_v = "0;0.31;1", "1;0;0"
        else:
            op_kt, op_v = f"0;{a:.4f};{a + 0.31:.4f};1", "0;1;0;0"
        cursors.append(
            f'<g class="cur"><rect y="268" width="8" height="19" fill="%TEAL%" x="84" opacity="0">'
            f'<animate attributeName="x" dur="20s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt_s}" values="{";".join(map(str, xs))}"/>'
            f'<animate attributeName="opacity" dur="20s" repeatCount="indefinite" calcMode="discrete" keyTimes="{op_kt}" values="{op_v}"/>'
            f"</rect></g>"
        )
    chips, x = [], 48
    for j, label in enumerate(["Codeforces Pupil", "IT Engineering", "Building Converge"]):
        w = int(len(label) * 7.4 + 30)
        chips.append(
            f'<g class="fu" style="animation-delay:{0.6 + j * 0.12:.2f}s">'
            f'<rect x="{x + .5}" y="172.5" width="{w}" height="26" rx="13" fill="#161f33" stroke="%LINE%"/>'
            f'<circle cx="{x + 14}" cy="185.5" r="3" fill="%TEAL%"/>'
            f'<text class="chip" x="{x + 24}" y="190">{esc(label)}</text></g>'
        )
        x += w + 10
    svg = HERO.replace("__CLIPS__", "".join(clips)).replace("__STARS__", stars)
    svg = svg.replace("__TEXTS__", "".join(texts)).replace("__CURSORS__", "".join(cursors))
    svg = svg.replace("__CHIPS__", "".join(chips))
    save("hero.svg", tpl(svg))


# ───────────────────────── HEADINGS ─────────────────────────
HEAD = """
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="56" viewBox="0 0 900 56" role="img" aria-label="%TITLE%">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="%VIOLET%"/><stop offset="1" stop-color="%TEAL%"/></linearGradient></defs>
<style>
.n{font:600 13px %MONO%;fill:%AMBER%;letter-spacing:2px}
.t{font:800 24px %SANS%;fill:%TEXT%}
.s{font:500 13px %MONO%;fill:%MUTED%}
.bar{transform-box:fill-box;transform-origin:left;animation:grow 1.6s cubic-bezier(.2,.8,.2,1) both}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.dot{animation:pulse 2s ease-in-out infinite}
@keyframes pulse{50%{opacity:.25}}
</style>
<rect x=".5" y=".5" width="899" height="55" rx="12" fill="%BG%" stroke="%LINE%"/>
<circle class="dot" cx="26" cy="28" r="4" fill="%AMBER%"/>
<text class="n" x="42" y="33">%NUM%</text>
<text class="t" x="104" y="36">%TITLE%</text>
<text class="s" x="874" y="33" text-anchor="end">%SUB%</text>
<rect class="bar" x="14" y="51" width="872" height="3" rx="1.5" fill="url(#g)"/>
</svg>
"""


def headings():
    for slug, num, title, sub in [
        ("about", "// 01", "About me", "observe"),
        ("cases", "// 02", "Case files", "deduce"),
        ("palace", "// 03", "Mind palace", "remember"),
        ("stats", "// 04", "Live stats", "evidence"),
        ("activity", "// 05", "Activity", "patterns"),
    ]:
        save(f"heading-{slug}.svg", tpl(HEAD, NUM=num, TITLE=title, SUB=sub))


# ───────────────────────── CASE CARDS ─────────────────────────
CARD = """
<svg xmlns="http://www.w3.org/2000/svg" width="280" height="176" viewBox="0 0 280 176" role="img" aria-label="%TITLE%: %ARIA%">
<style>
.no{font:600 11px %MONO%;letter-spacing:2px;fill:%AMBER%}
.st{font:600 10px %MONO%;letter-spacing:1.5px;fill:%SC%}
.ti{font:800 22px %SANS%;fill:%TEXT%}
.de{font:500 12.5px %SANS%;fill:%MUTED%}
.tg{font:600 11px %SANS%;fill:%TEXT%}
.bd{fill:none;stroke:%SC%;stroke-width:1.6;stroke-linecap:round;stroke-dasharray:90 790;animation:run 5s linear infinite}
@keyframes run{to{stroke-dashoffset:-880}}
.pl{animation:pulse 1.6s ease-in-out infinite}
@keyframes pulse{50%{opacity:.2}}
.fu{opacity:0;animation:fu .8s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes fu{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
</style>
<rect x="1" y="1" width="278" height="174" rx="14" fill="%PANEL%" stroke="%LINE%"/>
<rect class="bd" x="1" y="1" width="278" height="174" rx="14"/>
<g class="fu" style="animation-delay:.1s">
  <text class="no" x="20" y="32">CASE %NUM%</text>
  <circle class="pl" cx="%DOTX%" cy="28" r="3.5" fill="%SC%"/>
  <text class="st" x="262" y="32" text-anchor="end">%STATUS%</text>
</g>
<text class="ti fu" x="20" y="68" style="animation-delay:.2s">%TITLE%</text>
<g class="fu" style="animation-delay:.3s"><text class="de" x="20" y="92">%L1%</text><text class="de" x="20" y="110">%L2%</text></g>
%TAGS%
</svg>
"""


def card(slug, num, status, sc, title, l1, l2, tags):
    tag_svg, x = [], 20
    for j, t in enumerate(tags):
        w = int(len(t) * 6.3 + 20)
        tag_svg.append(
            f'<g class="fu" style="animation-delay:{0.4 + j * 0.1:.1f}s"><rect x="{x + .5}" y="134.5" width="{w}" height="22" rx="11" fill="#161f33" stroke="%LINE%"/>'
            f'<text class="tg" x="{x + w / 2}" y="149" text-anchor="middle">{esc(t)}</text></g>'
        )
        x += w + 8
    dotx = 262 - int(len(status) * 7.4 + 12)
    save(
        f"card-{slug}.svg",
        tpl(CARD, NUM=num, STATUS=status, SC=sc, TITLE=esc(title), ARIA=esc(l1 + " " + l2),
            L1=esc(l1), L2=esc(l2), TAGS="".join(tag_svg), DOTX=dotx),
    )


def cards():
    card("converge", "#001", "IN PROGRESS", "#22c55e", "Converge",
         "A shared whiteboard where teams", "think together, live.", ["React", "tldraw", "Node.js"])
    card("url", "#002", "ON GITHUB", "#8b7cff", "URL Shortener",
         "Turn long links into short,", "tidy ones you can share.", ["Web app", "Backend"])
    card("ai", "#003", "OPEN", "#f59e0b", "Converge AI",
         "Next lead: an assistant that", "helps teams on the board.", ["AI", "Next up"])


# ───────────────────────── MIND PALACE ─────────────────────────
def palace():
    rooms = [
        ("ROOM 01", "The Atrium", "Frontend", ["React · Vite", "Tailwind CSS", "HTML · CSS"], "#8b7cff"),
        ("ROOM 02", "The Engine Room", "Backend & data", ["Node.js · Express", "MongoDB", "Firebase"], "#2dd4bf"),
        ("ROOM 03", "The Library", "Algorithms", ["Data structures", "Codeforces", "LeetCode"], "#f59e0b"),
        ("ROOM 04", "The Gatehouse", "Security", ["Authentication", "Cookie sessions", "Protected rooms"], "#f472b6"),
        ("ROOM 05", "The Dock", "Shipping", ["Git · GitHub", "Vercel", "Render"], "#60a5fa"),
    ]
    out = []
    for i, (num, name, sub, items, col) in enumerate(rooms):
        x = i * 184
        its = "".join(
            f'<text class="it" x="{x + 16}" y="{118 + j * 22}"><tspan fill="{col}">›</tspan> {esc(t)}</text>'
            for j, t in enumerate(items)
        )
        out.append(
            f'<g class="fu" style="animation-delay:{i * 0.12:.2f}s">'
            f'<rect x="{x + .5}" y="10.5" width="163" height="169" rx="14" fill="%PANEL%" stroke="%LINE%"/>'
            f'<rect class="lit" x="{x + .5}" y="10.5" width="163" height="169" rx="14" fill="{col}" stroke="{col}" style="animation-delay:{i * 1.4}s"/>'
            f'<path d="M{x + 126} 44 v-14 a11 11 0 0 1 22 0 v14 z" fill="none" stroke="{col}" stroke-opacity=".8"/>'
            f'<text class="rm" x="{x + 16}" y="36" fill="{col}">{num}</text>'
            f'<text class="rn" x="{x + 16}" y="64">{esc(name)}</text>'
            f'<text class="sb" x="{x + 16}" y="82">{esc(sub)}</text>'
            f'<line x1="{x + 16}" y1="94" x2="{x + 147}" y2="94" stroke="%LINE%"/>{its}</g>'
        )
    svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="190" viewBox="0 0 900 190" role="img" aria-label="Mind palace: skills organised as five rooms">
<style>
.rm{font:600 11px %MONO%;letter-spacing:2px}
.rn{font:800 16px %SANS%;fill:%TEXT%}
.sb{font:500 12px %SANS%;fill:%MUTED%}
.it{font:500 12.5px %SANS%;fill:%TEXT%}
.lit{fill-opacity:0;stroke-opacity:.15;animation:lit 7s ease-in-out infinite}
@keyframes lit{0%{fill-opacity:0;stroke-opacity:.15}6%,16%{fill-opacity:.09;stroke-opacity:1}26%,100%{fill-opacity:0;stroke-opacity:.15}}
.fu{opacity:0;animation:fu .8s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes fu{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
</style>
""" + "".join(out) + "</svg>"
    save("palace.svg", tpl(svg))


# ───────────────────────── FOOTER ─────────────────────────
def footer():
    wave = "M0 66 Q75 40 150 66 T300 66 T450 66 T600 66 T750 66 T900 66 T1050 66 T1200 66 V100 H0 Z"
    svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="100" viewBox="0 0 900 100" role="img" aria-label="Observe. Deduce. Ship.">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="%VIOLET%"/><stop offset="1" stop-color="%TEAL%"/></linearGradient></defs>
<style>
.f{font:600 15px %MONO%;letter-spacing:3px;fill:%TEAL%;animation:pulse 3s ease-in-out infinite}
@keyframes pulse{50%{opacity:.55}}
</style>
<text class="f" x="450" y="32" text-anchor="middle">OBSERVE · DEDUCE · SHIP</text>
<path d="__WAVE__" fill="url(#g)" opacity=".35"><animateTransform attributeName="transform" type="translate" from="0 0" to="-300 0" dur="9s" repeatCount="indefinite"/></path>
<path d="__WAVE__" fill="url(#g)" opacity=".6"><animateTransform attributeName="transform" type="translate" from="-300 8" to="0 8" dur="6s" repeatCount="indefinite"/></path>
</svg>
""".replace("__WAVE__", wave)
    save("footer.svg", tpl(svg))


if __name__ == "__main__":
    hero(); headings(); cards(); palace(); footer()
