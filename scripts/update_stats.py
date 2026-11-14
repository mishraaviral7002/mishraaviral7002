#!/usr/bin/env python3
"""Fetch live Codeforces + LeetCode stats and render them as animated SVG cards.

The Codeforces handle is read from the CF_HANDLE environment variable (a GitHub
Actions secret), is never written into any file, and is never printed.
Set DEMO=1 to render placeholder cards without any network access.
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
ASSETS.mkdir(exist_ok=True)
CF_HANDLE = os.environ.get("CF_HANDLE", "").strip()
LC_USER = os.environ.get("LC_USER", "aviralmishra9876").strip()
DEMO = os.environ.get("DEMO") == "1"

C = dict(
    SANS="'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif",
    MONO="'Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace",
    BG="#0b1018", PANEL="#0e1524", LINE="#1f2a3d",
    VIOLET="#8b7cff", TEAL="#2dd4bf", AMBER="#f59e0b", TEXT="#e6edf7", MUTED="#9fb0c8",
)

RANK_COL = {
    "unrated": "#9fb0c8", "newbie": "#9ca3af", "pupil": "#22c55e", "specialist": "#2dd4bf",
    "expert": "#6b8cff", "candidate master": "#c084fc", "master": "#fb923c",
    "international master": "#fb923c", "grandmaster": "#f87171",
    "international grandmaster": "#f87171", "legendary grandmaster": "#f87171",
}


def tpl(s, **kw):
    for k, v in {**C, **kw}.items():
        s = s.replace(f"%{k}%", str(v))
    return s


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt(v, prefix=""):
    return "—" if v is None else f"{prefix}{v:,}" if isinstance(v, int) else str(v)


def plain(v):
    return "—" if v is None else str(v)


def http_json(url, data=None, headers=None, tries=3):
    # Never print the URL or the exception: either could contain the handle.
    for i in range(tries):
        try:
            req = urllib.request.Request(
                url, data=data,
                headers={"User-Agent": "Mozilla/5.0 (profile-readme-bot)", **(headers or {})},
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception:
            time.sleep(3 * (i + 1))
    return None


# ───────────────────────── fetchers ─────────────────────────
def cf_call(method, **params):
    d = http_json(f"https://codeforces.com/api/{method}?{urllib.parse.urlencode(params)}")
    return d["result"] if d and d.get("status") == "OK" else None


def fetch_codeforces():
    info = cf_call("user.info", handles=CF_HANDLE)
    if not info:
        return None
    u = info[0]
    hist = cf_call("user.rating", handle=CF_HANDLE) or []
    subs = cf_call("user.status", handle=CF_HANDLE, **{"from": 1, "count": 100000}) or []
    solved = {(s["problem"].get("contestId"), s["problem"]["index"]) for s in subs if s.get("verdict") == "OK"}
    return dict(
        rating=u.get("rating", 0), max_rating=u.get("maxRating", 0),
        rank=u.get("rank", "unrated"), max_rank=u.get("maxRank", "unrated"),
        contests=len(hist), solved=len(solved),
        series=[h["newRating"] for h in hist][-40:],
    )


LC_QUERY = """query u($u:String!){
  matchedUser(username:$u){profile{ranking} submitStatsGlobal{acSubmissionNum{difficulty count}}}
  allQuestionsCount{difficulty count}
  userContestRanking(username:$u){rating attendedContestsCount}
}"""


def fetch_leetcode():
    d = http_json(
        "https://leetcode.com/graphql",
        data=json.dumps({"query": LC_QUERY, "variables": {"u": LC_USER}}).encode(),
        headers={"Content-Type": "application/json", "Referer": "https://leetcode.com"},
    )
    try:
        data = d["data"]
        mu = data["matchedUser"]
        solved = {x["difficulty"]: x["count"] for x in mu["submitStatsGlobal"]["acSubmissionNum"]}
        totals = {x["difficulty"]: x["count"] for x in data["allQuestionsCount"]}
        ct = data.get("userContestRanking") or {}
        return dict(
            solved=solved.get("All"), easy=solved.get("Easy"), medium=solved.get("Medium"), hard=solved.get("Hard"),
            easy_t=totals.get("Easy"), medium_t=totals.get("Medium"), hard_t=totals.get("Hard"),
            ranking=mu["profile"].get("ranking"),
            contest=int(ct["rating"]) if ct.get("rating") else None,
            contests=ct.get("attendedContestsCount"),
        )
    except Exception:
        return None


# ───────────────────────── renderers ─────────────────────────
CF_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="430" height="200" viewBox="0 0 430 200" role="img" aria-label="Live competitive programming rating card">
<defs>
  <linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%COL%" stop-opacity=".35"/><stop offset="1" stop-color="%COL%" stop-opacity="0"/></linearGradient>
</defs>
<style>
.hd{font:600 11px %MONO%;letter-spacing:2px;fill:%MUTED%}
.big{font:800 56px %SANS%;fill:%COL%}
.rk{font:700 13px %MONO%;letter-spacing:3px;fill:%COL%}
.lb{font:600 10px %MONO%;letter-spacing:1.5px;fill:%MUTED%}
.vl{font:800 18px %SANS%;fill:%TEXT%}
.st{font:500 9px %MONO%;fill:#5b6b88}
.pl{animation:pulse 1.6s ease-in-out infinite}
@keyframes pulse{50%{opacity:.2}}
.fu{opacity:0;animation:fu .8s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes fu{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.line{fill:none;stroke:%COL%;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:draw 2.2s .3s ease forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.area{opacity:0;animation:fade 1s 1.8s forwards}
@keyframes fade{to{opacity:1}}
.ring{transform-box:fill-box;transform-origin:center;animation:ping 2s ease-out infinite}
@keyframes ping{0%{transform:scale(1);opacity:.7}100%{transform:scale(3);opacity:0}}
</style>
<rect x=".5" y=".5" width="429" height="199" rx="14" fill="%PANEL%" stroke="%LINE%"/>
<circle class="pl" cx="26" cy="23" r="4" fill="#22c55e"/>
<text class="hd" x="38" y="27">CODEFORCES · LIVE</text>
<g class="fu" style="animation-delay:.1s"><text class="big" x="22" y="92">%RATING%</text><text class="rk" x="26" y="116">%RANK%</text></g>
<g class="fu" style="animation-delay:.25s">
  <text class="lb" x="236" y="48">MAX RATING</text><text class="vl" x="236" y="70">%MAXR%</text>
  <text class="lb" x="330" y="48">MAX RANK</text><text class="vl" x="330" y="70" style="font-size:14px">%MAXRANK%</text>
  <text class="lb" x="236" y="94">CONTESTS</text><text class="vl" x="236" y="116">%CONTESTS%</text>
  <text class="lb" x="330" y="94">SOLVED</text><text class="vl" x="330" y="116">%SOLVED%</text>
</g>
<path class="area" d="%AREA%" fill="url(#ar)"/>
<path class="line" pathLength="1" d="%LINE_D%"/>
<circle cx="%EX%" cy="%EY%" r="3.5" fill="%COL%"/>
<circle class="ring" cx="%EX%" cy="%EY%" r="3.5" fill="none" stroke="%COL%"/>
<text class="st" x="406" y="192" text-anchor="end">%STAMP%</text>
</svg>
"""


def render_cf(d, stamp):
    rank = (d["rank"] or "unrated").lower()
    col = RANK_COL.get(rank, "#9fb0c8")
    series = list(d["series"]) or [d["rating"], d["rating"]]
    if len(series) < 2:
        series = series * 2
    x0, x1, y0, y1 = 24, 406, 140, 176
    lo, hi = min(series), max(series)
    pts = []
    for i, v in enumerate(series):
        x = x0 + (x1 - x0) * i / (len(series) - 1)
        y = (y0 + y1) / 2 if hi == lo else y1 - (y1 - y0) * (v - lo) / (hi - lo)
        pts.append((x, y))
    line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    area = f"{line} L{x1} 182 L{x0} 182 Z"
    return tpl(
        CF_SVG, COL=col, RATING=plain(d["rating"]), RANK=esc(rank.upper()),
        MAXR=plain(d["max_rating"]), MAXRANK=esc((d["max_rank"] or "—").title()),
        CONTESTS=fmt(d["contests"]), SOLVED=fmt(d["solved"]),
        LINE_D=line, AREA=area, EX=f"{pts[-1][0]:.1f}", EY=f"{pts[-1][1]:.1f}", STAMP=esc(stamp),
    )


LC_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="430" height="200" viewBox="0 0 430 200" role="img" aria-label="Live LeetCode stats card">
<style>
.hd{font:600 11px %MONO%;letter-spacing:2px;fill:%MUTED%}
.big{font:800 56px %SANS%;fill:%TEXT%}
.lb{font:600 10px %MONO%;letter-spacing:1.5px;fill:%MUTED%}
.vl{font:800 18px %SANS%;fill:%TEXT%}
.dl{font:600 12px %SANS%}
.ct{font:500 11px %MONO%;fill:%MUTED%}
.st{font:500 9px %MONO%;fill:#5b6b88}
.pl{animation:pulse 1.6s ease-in-out infinite}
@keyframes pulse{50%{opacity:.2}}
.fu{opacity:0;animation:fu .8s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes fu{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
</style>
<rect x=".5" y=".5" width="429" height="199" rx="14" fill="%PANEL%" stroke="%LINE%"/>
<circle class="pl" cx="26" cy="23" r="4" fill="%AMBER%"/>
<text class="hd" x="38" y="27">LEETCODE · LIVE</text>
<g class="fu" style="animation-delay:.1s"><text class="big" x="22" y="92">%SOLVED%</text><text class="lb" x="26" y="116">PROBLEMS SOLVED</text></g>
%ROWS%
<g class="fu" style="animation-delay:.4s">
  <text class="lb" x="26" y="146">GLOBAL RANK</text><text class="vl" x="26" y="168">%RANK%</text>
  <text class="lb" x="170" y="146">CONTEST RATING</text><text class="vl" x="170" y="168">%CONTEST%</text>
</g>
<text class="st" x="406" y="192" text-anchor="end">%STAMP%</text>
</svg>
"""


def render_lc(d, stamp):
    rows = []
    spec = [("Easy", "#22c55e", d.get("easy"), d.get("easy_t")),
            ("Medium", "#f59e0b", d.get("medium"), d.get("medium_t")),
            ("Hard", "#ef4444", d.get("hard"), d.get("hard_t"))]
    for i, (lab, col, cnt, tot) in enumerate(spec):
        y = 52 + i * 30
        frac = (cnt / tot) if (cnt is not None and tot) else 0
        bw = round(170 * frac, 1)
        rows.append(
            f'<g class="fu" style="animation-delay:{0.2 + i * 0.1:.1f}s">'
            f'<text class="dl" x="236" y="{y}" fill="{col}">{lab}</text>'
            f'<text class="ct" x="406" y="{y}" text-anchor="end">{fmt(cnt)}{" / " + fmt(tot) if tot else ""}</text>'
            f'<rect x="236" y="{y + 8}" width="170" height="6" rx="3" fill="#161f33"/>'
            f'<rect x="236" y="{y + 8}" width="0" height="6" rx="3" fill="{col}">'
            f'<animate attributeName="width" from="0" to="{bw}" dur="1.3s" begin="{0.5 + i * 0.15:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect></g>'
        )
    return tpl(LC_SVG, SOLVED=fmt(d.get("solved")), ROWS="".join(rows),
               RANK=fmt(d.get("ranking"), "#"), CONTEST=plain(d.get("contest")), STAMP=esc(stamp))


# ───────────────────────── main ─────────────────────────
def main():
    stamp = "updated " + datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if DEMO:
        cf = dict(rating=1235, max_rating=None, rank="pupil", max_rank=None, contests=None, solved=None, series=[1235, 1235])
        lc = dict(solved=None, ranking=None, contest=None)
        stamp = "awaiting first sync"
    else:
        cf = fetch_codeforces() if CF_HANDLE else None
        lc = fetch_leetcode()
    if cf:
        (ASSETS / "codeforces.svg").write_text(render_cf(cf, stamp), encoding="utf-8")
        print("Codeforces card updated")
    else:
        print("Codeforces card NOT updated (missing secret or API unreachable)")
    if lc:
        (ASSETS / "leetcode.svg").write_text(render_lc(lc, stamp), encoding="utf-8")
        print("LeetCode card updated")
    else:
        print("LeetCode card NOT updated (API unreachable)")


if __name__ == "__main__":
    main()
