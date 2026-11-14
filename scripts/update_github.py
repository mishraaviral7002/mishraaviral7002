#!/usr/bin/env python3
"""Render GitHub stats, top languages and contribution activity as animated SVG cards.

Uses the GitHub GraphQL API with the built-in GITHUB_TOKEN (no outside services).
Set DEMO=1 to render placeholder cards without any network access.
"""
import json
import os
import time
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
ASSETS.mkdir(exist_ok=True)
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
USER = (os.environ.get("GH_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "mishraaviral7002").strip()
DEMO = os.environ.get("DEMO") == "1"

C = dict(
    SANS="'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif",
    MONO="'Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace",
    BG="#0b1018", PANEL="#0e1524", LINE="#1f2a3d",
    VIOLET="#8b7cff", TEAL="#2dd4bf", AMBER="#f59e0b", TEXT="#e6edf7", MUTED="#9fb0c8",
)
FALLBACK = ["#8b7cff", "#2dd4bf", "#f59e0b", "#f472b6", "#60a5fa", "#9ca3af"]


def tpl(s, **kw):
    for k, v in {**C, **kw}.items():
        s = s.replace(f"%{k}%", str(v))
    return s


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def num(v):
    return "—" if v is None else f"{v:,}"


QUERY = """query($login:String!){
 user(login:$login){
  followers{totalCount}
  pullRequests{totalCount}
  repositories(first:100, ownerAffiliations:OWNER, isFork:false){
    totalCount
    nodes{ stargazerCount languages(first:8, orderBy:{field:SIZE,direction:DESC}){ edges{ size node{ name color } } } }
  }
  contributionsCollection{
    totalCommitContributions restrictedContributionsCount
    contributionCalendar{ totalContributions weeks{ contributionDays{ contributionCount date } } }
  }
 }
}"""


def fetch():
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    for i in range(3):
        try:
            req = urllib.request.Request(
                "https://api.github.com/graphql", data=body,
                headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json",
                         "User-Agent": "profile-readme-bot"})
            with urllib.request.urlopen(req, timeout=30) as r:
                u = json.load(r)["data"]["user"]
            break
        except Exception:
            u = None
            time.sleep(3 * (i + 1))
    if not u:
        return None
    repos = u["repositories"]["nodes"]
    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]
            d = langs.setdefault(n["name"], [0, n.get("color")])
            d[0] += e["size"]
    cc = u["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    today = date.today()
    counts = {d["date"]: d["contributionCount"] for d in days}
    cur, day = 0, today
    if counts.get(day.isoformat(), 0) == 0:  # today may not have activity yet
        day -= timedelta(days=1)
    while counts.get(day.isoformat(), 0) > 0:
        cur += 1
        day -= timedelta(days=1)
    return dict(
        stars=sum(r["stargazerCount"] for r in repos),
        commits=cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        prs=u["pullRequests"]["totalCount"], repos=u["repositories"]["totalCount"],
        followers=u["followers"]["totalCount"], streak=cur,
        langs=sorted(((k, v[0], v[1]) for k, v in langs.items()), key=lambda x: -x[1]),
        total=cc["contributionCalendar"]["totalContributions"],
        weeks=[(w["contributionDays"][0]["date"], sum(d["contributionCount"] for d in w["contributionDays"]))
               for w in cc["contributionCalendar"]["weeks"] if w["contributionDays"]],
    )


BASE_CSS = """
.hd{font:600 11px %MONO%;letter-spacing:2px;fill:%MUTED%}
.lb{font:600 10px %MONO%;letter-spacing:1.5px;fill:%MUTED%}
.vl{font:800 30px %SANS%;fill:%TEXT%}
.st{font:500 9px %MONO%;fill:#5b6b88}
.pl{animation:pulse 1.6s ease-in-out infinite}
@keyframes pulse{50%{opacity:.2}}
.fu{opacity:0;animation:fu .8s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes fu{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
"""

# ───────────── stats card ─────────────
def render_stats(d, stamp):
    items = [("STARS", d.get("stars")), ("COMMITS · 1Y", d.get("commits")), ("PULL REQUESTS", d.get("prs")),
             ("REPOSITORIES", d.get("repos")), ("FOLLOWERS", d.get("followers")), ("DAY STREAK", d.get("streak"))]
    cols = [C["AMBER"], C["TEAL"], C["VIOLET"], C["TEXT"], C["TEXT"], "#22c55e"]
    out = []
    for i, ((lab, val), col) in enumerate(zip(items, cols)):
        x, y = 24 + (i % 3) * 136, 64 + (i // 3) * 64
        out.append(f'<g class="fu" style="animation-delay:{0.1 + i * 0.08:.2f}s"><text class="lb" x="{x}" y="{y}">{lab}</text>'
                   f'<text class="vl" x="{x}" y="{y + 30}" style="fill:{col}">{num(val)}</text></g>')
    svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="430" height="200" viewBox="0 0 430 200" role="img" aria-label="GitHub stats card">
<style>%CSS%</style>
<rect x=".5" y=".5" width="429" height="199" rx="14" fill="%PANEL%" stroke="%LINE%"/>
<circle class="pl" cx="26" cy="23" r="4" fill="#22c55e"/><text class="hd" x="38" y="27">GITHUB · LIVE</text>
%ITEMS%
<text class="st" x="406" y="192" text-anchor="end">%STAMP%</text>
</svg>"""
    return tpl(svg, CSS=tpl(BASE_CSS), ITEMS="".join(out), STAMP=esc(stamp))


# ───────────── languages card ─────────────
def render_langs(d, stamp):
    langs = d.get("langs") or []
    total = sum(s for _, s, _ in langs) or 1
    top = langs[:5]
    other = sum(s for _, s, _ in langs[5:])
    segs = [(n, s, c or FALLBACK[i % 5]) for i, (n, s, c) in enumerate(top)]
    if other:
        segs.append(("Other", other, FALLBACK[5]))
    bar, legend, x = [], [], 24.0
    for i, (n, s, c) in enumerate(segs):
        w = 382 * s / total
        bar.append(f'<rect x="{x:.1f}" y="48" width="{max(w - 2, 1):.1f}" height="12" fill="{c}"/>')
        x += w
        lx, ly = 24 + (i % 2) * 202, 96 + (i // 2) * 28
        legend.append(f'<g class="fu" style="animation-delay:{0.3 + i * 0.08:.2f}s"><circle cx="{lx + 4}" cy="{ly - 4}" r="4" fill="{c}"/>'
                      f'<text class="nm" x="{lx + 16}" y="{ly}">{esc(n)}</text>'
                      f'<text class="pc" x="{lx + 180}" y="{ly}" text-anchor="end">{100 * s / total:.1f}%</text></g>')
    empty = "" if segs else '<text class="st" x="24" y="100">awaiting first sync</text>'
    svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="430" height="200" viewBox="0 0 430 200" role="img" aria-label="Top languages card">
<defs><clipPath id="rev"><rect x="24" y="44" width="0" height="20" rx="6"><animate attributeName="width" from="0" to="382" dur="1.4s" begin=".2s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect></clipPath></defs>
<style>%CSS%
.nm{font:600 13px %SANS%;fill:%TEXT%}
.pc{font:500 12px %MONO%;fill:%MUTED%}
</style>
<rect x=".5" y=".5" width="429" height="199" rx="14" fill="%PANEL%" stroke="%LINE%"/>
<circle class="pl" cx="26" cy="23" r="4" fill="%VIOLET%"/><text class="hd" x="38" y="27">TOP LANGUAGES · LIVE</text>
<rect x="24" y="48" width="382" height="12" rx="6" fill="#161f33"/>
<g clip-path="url(#rev)">%BAR%</g>
%LEGEND%%EMPTY%
<text class="st" x="406" y="192" text-anchor="end">%STAMP%</text>
</svg>"""
    return tpl(svg, CSS=tpl(BASE_CSS), BAR="".join(bar), LEGEND="".join(legend), EMPTY=empty, STAMP=esc(stamp))


# ───────────── activity graph ─────────────
def render_activity(d, stamp):
    weeks = d.get("weeks") or []
    vals = [v for _, v in weeks] or [0, 0]
    if len(vals) < 2:
        vals = vals * 2
    x0, x1, y0, y1 = 24, 876, 66, 150
    hi = max(max(vals), 1)
    pts = [(x0 + (x1 - x0) * i / (len(vals) - 1), y1 - (y1 - y0) * v / hi) for i, v in enumerate(vals)]
    line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    area = f"{line} L{x1} {y1 + 4} L{x0} {y1 + 4} Z"
    months, last = [], None
    for i, (dt, _) in enumerate(weeks):
        m = datetime.strptime(dt, "%Y-%m-%d").strftime("%b")
        if m != last and (i == 0 or i < len(weeks) - 2):
            months.append(f'<text class="mo" x="{pts[i][0]:.1f}" y="176">{m}</text>')
        last = m
    peak = max(range(len(vals)), key=lambda i: vals[i])
    svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="200" viewBox="0 0 900 200" role="img" aria-label="Contribution activity graph">
<defs><linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%TEAL%" stop-opacity=".4"/><stop offset="1" stop-color="%TEAL%" stop-opacity="0"/></linearGradient>
<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="%VIOLET%"/><stop offset="1" stop-color="%TEAL%"/></linearGradient></defs>
<style>%CSS%
.tot{font:800 16px %SANS%;fill:%TEXT%}
.mo{font:500 10px %MONO%;fill:#5b6b88}
.line{fill:none;stroke:url(#ln);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:draw 2.6s .3s ease forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.area{opacity:0;animation:fade 1s 2s forwards}
@keyframes fade{to{opacity:1}}
.ring{transform-box:fill-box;transform-origin:center;animation:ping 2s ease-out infinite}
@keyframes ping{0%{transform:scale(1);opacity:.7}100%{transform:scale(3);opacity:0}}
</style>
<rect x=".5" y=".5" width="899" height="199" rx="14" fill="%PANEL%" stroke="%LINE%"/>
<circle class="pl" cx="26" cy="23" r="4" fill="%TEAL%"/><text class="hd" x="38" y="27">CONTRIBUTION ACTIVITY · LIVE</text>
<text class="tot" x="876" y="28" text-anchor="end">%TOTAL%</text>
<text class="mo" x="%LABX%" y="28" text-anchor="end" style="font-size:12px;fill:%MUTED%">contributions in the last year</text>
<line x1="24" y1="154" x2="876" y2="154" stroke="%LINE%"/>
<path class="area" d="%AREA%" fill="url(#ar)"/>
<path class="line" pathLength="1" d="%LINE%"/>
<circle cx="%PX%" cy="%PY%" r="3.5" fill="%TEAL%"/><circle class="ring" cx="%PX%" cy="%PY%" r="3.5" fill="none" stroke="%TEAL%"/>
<text class="mo" x="%PX%" y="%PYT%" text-anchor="middle" style="fill:%MUTED%">peak week · %PEAK%</text>
%MONTHS%
<text class="st" x="876" y="192" text-anchor="end">%STAMP%</text>
</svg>"""
    return tpl(svg, CSS=tpl(BASE_CSS), TOTAL=num(d.get("total")), LABX=876 - len(num(d.get("total"))) * 11 - 12, AREA=area, LINE=line,
               PX=f"{pts[peak][0]:.1f}", PY=f"{pts[peak][1]:.1f}", PYT=f"{max(pts[peak][1] - 10, 46):.1f}",
               PEAK=vals[peak], MONTHS="".join(months), STAMP=esc(stamp))


def main():
    stamp = "updated " + datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if DEMO:
        d = dict(total=None, weeks=[], langs=[])
        stamp = "awaiting first sync"
    else:
        d = fetch() if TOKEN else None
    if not d:
        print("GitHub cards NOT updated (missing token or API unreachable)")
        return
    for name, fn in [("github-stats.svg", render_stats), ("languages.svg", render_langs), ("activity.svg", render_activity)]:
        (ASSETS / name).write_text(fn(d, stamp), encoding="utf-8")
    print("GitHub cards updated")


if __name__ == "__main__":
    main()
