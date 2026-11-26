#!/usr/bin/env python3
"""Builds the static, animated SVG assets (hero, headings, case cards, mind palace, footer)."""
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

C = dict(
    SANS="'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif",
    MONO="'Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace",
    BG="#0c0a0a", BG2="#1a0f0f", PANEL="#120d0d", LINE="#2e1c1c",
    VIOLET="#ef4444", TEAL="#fb923c", AMBER="#f59e0b", TEXT="#f3ece8", MUTED="#b8a9a3",
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
  <radialGradient id="eye" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#fff3c4"/><stop offset=".35" stop-color="#fbbf24"/><stop offset="1" stop-color="#ea580c"/></radialGradient>
  <radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ea580c" stop-opacity=".45"/><stop offset="1" stop-color="#ea580c" stop-opacity="0"/></radialGradient>
  <linearGradient id="tyg" x1="0" x2="1"><stop offset="0" stop-color="%VIOLET%"/><stop offset="1" stop-color="%AMBER%"/></linearGradient>
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
.fl{animation:fl 2.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes fl{0%,100%{opacity:.65;transform:scale(1)}50%{opacity:1;transform:scale(1.12)}}
.bl{animation:bl 6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes bl{0%,90%,100%{transform:scaleY(1)}94%{transform:scaleY(.06)}}
.em{opacity:0;animation:em 4s linear infinite}
@keyframes em{0%{opacity:0;transform:translateY(0)}15%{opacity:.9}100%{opacity:0;transform:translateY(-110px)}}
.sp{animation:sp 7s ease-in-out infinite}
@keyframes sp{50%{opacity:.6}}
.tt{font:800 18px %SANS%;letter-spacing:5px;fill:url(#tyg)}
.pulse{animation:pulse 1.8s ease-in-out infinite}
@keyframes pulse{50%{opacity:.25}}
</style>

<rect width="900" height="340" rx="18" fill="url(#bg)"/>
<rect width="900" height="340" rx="18" fill="url(#grid)"/>
__STARS__

<!-- label, name, subtitle, chips -->
<g class="fu" style="animation-delay:.1s"><circle class="pulse" cx="52" cy="56" r="4" fill="%AMBER%"/><text class="lab" x="64" y="60">CASE FILE 001 · UNSOLVED</text></g>
<text class="nm fu" x="46" y="122" style="animation-delay:.25s">Aviral Mishra</text>
<text class="sub fu" x="48" y="154" style="animation-delay:.45s">Competitive programmer  ·  Full-stack developer</text>
__CHIPS__

<!-- cold-reading terminal -->
<g class="fu" style="animation-delay:.9s">
  <rect x="48.5" y="214.5" width="580" height="94" rx="10" fill="%PANEL%" stroke="%LINE%"/>
  <circle cx="68" cy="228" r="4" fill="#ef4444"/><circle cx="83" cy="228" r="4" fill="%AMBER%"/><circle cx="98" cy="228" r="4" fill="#22c55e"/>
  <text class="mono" x="116" y="232" font-size="11">calling_card.sh</text>
  <text class="mono" x="66" y="258"><tspan fill="%AMBER%">$</tspan> open case_file --unsolved</text>
  <text class="mono" x="66" y="284" style="fill:%AMBER%">&gt;</text>
  __TEXTS__
  __CURSORS__
</g>

__TYGER__
</svg>
"""


def tyger():
    rnd = random.Random(5)
    stripes = "".join(
        f'<path class="sp" style="animation-delay:{i * 0.9:.1f}s" d="M900 {y} L{x} {t} L900 {y + 16} Z" fill="#7f1d1d" opacity=".45"/>'
        for i, (y, x, t) in enumerate([(30, 820, 56), (92, 796, 114), (206, 808, 232), (268, 826, 292), (318, 846, 334)])
    )

    def eye(cx, flip):
        sc = "-1 1" if flip else "1 1"
        return (
            f'<g transform="translate({cx} 150) scale({sc})"><circle class="fl" r="52" fill="url(#halo)"/>'
            '<g class="bl"><path d="M-34 -4 Q-2 -24 30 6 Q-2 14 -34 -4 Z" fill="url(#eye)"/>'
            '<ellipse cx="-2" cy="1" rx="4.5" ry="11" fill="#0c0a0a"/><circle cx="-5" cy="-4" r="1.6" fill="#fff7d6"/></g></g>'
        )

    embers = "".join(
        f'<circle class="em" cx="{700 + i * 17}" cy="{236 + rnd.randint(0, 14)}" r="{rnd.choice([1.4, 1.8, 2.2])}" fill="#fbbf24" '
        f'style="animation-delay:{rnd.uniform(0, 4):.2f}s;animation-duration:{rnd.uniform(3, 5):.1f}s"/>'
        for i in range(11)
    )
    return (
        "<!-- the tyger -->" + stripes + eye(738, False) + eye(822, True) + embers
        + '<text class="tt fl" x="780" y="268" text-anchor="middle">TYGER TYGER</text>'
        + '<text class="mono" x="780" y="290" text-anchor="middle" style="font-size:10px;letter-spacing:3px">CASE STATUS · OPEN</text>'
    )


def hero():
    rnd = random.Random(11)
    stars = "".join(
        f'<circle class="tw" cx="{rnd.randint(24, 690)}" cy="{rnd.randint(14, 200)}" r="{rnd.choice([1, 1.2, 1.5])}" '
        f'fill="#ffd9b0" style="animation-delay:{rnd.uniform(0, 4):.2f}s"/>'
        for _ in range(26)
    )
    lines = [
        "Tyger Tyger. Someone left a mark on this page.",
        "Case status: unsolved. The evidence is in the repos.",
        "Prime suspect: a builder open to internships.",
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
            f'<rect x="{x + .5}" y="172.5" width="{w}" height="26" rx="13" fill="#1c1313" stroke="%LINE%"/>'
            f'<circle cx="{x + 14}" cy="185.5" r="3" fill="%TEAL%"/>'
            f'<text class="chip" x="{x + 24}" y="190">{esc(label)}</text></g>'
        )
        x += w + 10
    svg = HERO.replace("__CLIPS__", "".join(clips)).replace("__STARS__", stars)
    svg = svg.replace("__TEXTS__", "".join(texts)).replace("__CURSORS__", "".join(cursors))
    svg = svg.replace("__CHIPS__", "".join(chips)).replace("__TYGER__", tyger())
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
        ("about", "// 01", "About me", "the suspect"),
        ("cases", "// 02", "Case files", "open cases"),
        ("palace", "// 03", "Evidence room", "exhibits"),
        ("stats", "// 04", "Live stats", "surveillance"),
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
            f'<g class="fu" style="animation-delay:{0.4 + j * 0.1:.1f}s"><rect x="{x + .5}" y="134.5" width="{w}" height="22" rx="11" fill="#1c1313" stroke="%LINE%"/>'
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
    card("url", "#002", "ON GITHUB", "#ef4444", "URL Shortener",
         "Turn long links into short,", "tidy ones you can share.", ["Web app", "Backend"])
    card("ai", "#003", "OPEN", "#f59e0b", "Converge AI",
         "Next lead: an assistant that", "helps teams on the board.", ["AI", "Next up"])


# ───────────────────────── MIND PALACE ─────────────────────────
def palace():
    rooms = [
        ("EXHIBIT A", "The Facade", "Frontend", ["React · Vite", "Tailwind CSS", "HTML · CSS"], "#ef4444"),
        ("EXHIBIT B", "The Machinery", "Backend & data", ["Node.js · Express", "MongoDB", "Firebase"], "#fb923c"),
        ("EXHIBIT C", "The Archive", "Algorithms", ["Data structures", "Codeforces", "LeetCode"], "#f59e0b"),
        ("EXHIBIT D", "The Lockbox", "Security", ["Authentication", "Cookie sessions", "Protected rooms"], "#f472b6"),
        ("EXHIBIT E", "The Dock", "Shipping", ["Git · GitHub", "Vercel", "Render"], "#fbbf24"),
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
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="190" viewBox="0 0 900 190" role="img" aria-label="Evidence room: skills organised as five exhibits">
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
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="100" viewBox="0 0 900 100" role="img" aria-label="The case is still open">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="%VIOLET%"/><stop offset="1" stop-color="%TEAL%"/></linearGradient></defs>
<style>
.f{font:600 15px %MONO%;letter-spacing:3px;fill:%TEAL%;animation:pulse 3s ease-in-out infinite}
@keyframes pulse{50%{opacity:.55}}
</style>
<text class="f" x="450" y="32" text-anchor="middle">THE CASE IS STILL OPEN</text>
<path d="__WAVE__" fill="url(#g)" opacity=".35"><animateTransform attributeName="transform" type="translate" from="0 0" to="-300 0" dur="9s" repeatCount="indefinite"/></path>
<path d="__WAVE__" fill="url(#g)" opacity=".6"><animateTransform attributeName="transform" type="translate" from="-300 8" to="0 8" dur="6s" repeatCount="indefinite"/></path>
</svg>
""".replace("__WAVE__", wave)
    save("footer.svg", tpl(svg))


if __name__ == "__main__":
    hero(); headings(); cards(); palace(); footer()
