#!/usr/bin/env python3
"""
Builds assets/profile.svg from live GitHub data. Standard library only.

Design system:
  * Dark HUD / terminal poster: near-black ground, hairline rules, bracketed labels, mono type.
  * One accent colour (signal orange). Everything else is bone-white or grey.
  * Charts are plain bars and cells. Streak, heatmap and repo data are read live from GitHub.

Data sources (no token needed, a token only raises API limits):
  * contributions : https://github.com/users/<user>/contributions   (HTML calendar)
  * repositories  : GitHub REST API, falling back to the public repositories tab
"""
import calendar
import datetime as dt
import html
import json
import os
import random
import re
import sys
import textwrap
import urllib.request

# ───────────────────────── configuration ─────────────────────────
USER = os.environ.get("PROFILE_USER", "almostalok")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("PROFILE_OUT", os.path.join(HERE, "..", "assets", "profile.svg"))
PORTRAIT = os.path.join(HERE, "..", "assets", "portrait.txt")
OFFLINE = os.environ.get("PROFILE_OFFLINE_DIR")  # testing only: read saved HTML instead of the network

NAME_1, NAME_2 = "Alok Kumar", "Singh"
STATEMENT = ["Developer and product builder from India.",
             "Currently building Hospate, a hospital ERP.",
             "Ship > Perfection."]
PROFILE_ROWS = [
    ("Name", "Alok Kumar Singh"), ("Handle", "@almostalok"), ("Role", "Developer / Product Builder"),
    ("Building", "Hospate"), ("Location", "India"), ("Focus", "Useful products, real people"),
    ("Education", "Learning. Always."), ("Hobbies", "Code, Coffee, Ideas, Overthinking"),
    ("Fun fact", "My quick fixes become full features."),
]
STATUS = [("Hospate", "building", 90), ("System Design", "learning", 70), ("Product + Growth", "exploring", 60),
          ("Exciting problems", "open to", 80), ("Caffeine", "necessary", 100)]
ROLES = ["Reception", "Doctors", "Nurses", "Pharmacy", "Laboratory", "Radiology", "Billing", "Finance", "Admin", "HR", "Management"]
PIPELINE = ["idea", "product decision", "architecture", "code", "bug", "fix", "ship"]
STACK = [("Frontend", ["HTML", "CSS", "JS", "TS", "React", "Next", "Tailwind"]),
         ("Backend", ["Node", "Express", "NestJS", "Python", "Java", "GraphQL"]),
         ("Data / DevOps", ["MongoDB", "PostgreSQL", "MySQL", "Redis", "Docker", "AWS"]),
         ("Tools", ["Git", "Figma", "Jest", "Linux", "Electron", "Arduino", "Selenium"]),
         ("Mindset", ["frontend-first", "backend-driven discipline", "product-focused"])]
LINKS = [("Portfolio", "almostalok.tech"), ("Blog", "almostalokblogs.tech"), ("Resume", "almostalokresume.tech"),
         ("X", "@almostalok"), ("LinkedIn", "/in/alokkumarsingh"), ("Instagram", "@almostalok"), ("YouTube", "/c/almostalok")]
# repo name -> (title, one-line description). Dates and languages are read live.
FEATURED = [
    ("hospate_demo", "HospateOS", "Internal hospital ERP used daily across reception, clinical, pharmacy, lab, billing, HR and admin teams."),
    ("subguard", "SubGuard", "India-first recurring-payment guardian for UPI AutoPay, cards, standing instructions and subscriptions."),
    ("almosthack", "almosthack", "Transparent hackathon operating system with a developer-first aesthetic."),
    ("sync", "SiteSync", "Planning-to-reality platform for infrastructure projects. Smart India Hackathon 2026 entry."),
    ("Ray", "RAY", "Autonomous revenue-recovery and economic decision engine for Razorpay."),
    ("arm", "ARM", "AI-powered relationship management and a modern CRM platform."),
    ("tenant", "tenant", "Multi-tenant SaaS starter: schema-per-tenant Postgres, JWT auth, RBAC, Stripe billing."),
    ("bookify", "Bookify", "Book discovery, reading tracker and personal library platform."),
    ("devils-advocate", "Devil's Advocate", "Defend the undefendable. A minimalist debate and rhetoric crucible."),
]
SKIP_INDEX = {USER}  # repos left out of the "all repositories" index

# ───────────────────────── fetching ─────────────────────────
def http_get(url, accept="text/html", token=None):
    h = {"User-Agent": "profile-svg-builder", "Accept": accept}
    if token:
        h["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
        return r.read().decode("utf-8", "ignore")


def get_page(url, offline_name, **kw):
    if OFFLINE:
        p = os.path.join(OFFLINE, offline_name)
        return open(p, encoding="utf-8", errors="ignore").read() if os.path.exists(p) else ""
    return http_get(url, **kw)


def fetch_contributions():
    t = get_page(f"https://github.com/users/{USER}/contributions", "contrib.html")
    tips = {}
    for m in re.finditer(r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>([^<]+)</tool-tip>', t):
        s = m.group(2)
        n = re.match(r"\s*(\d+)\s+contribution", s)
        tips[m.group(1)] = int(n.group(1)) if n else 0
    days = {}
    for m in re.finditer(r"<td\b[^>]*>", t):
        tag = m.group(0)
        d = re.search(r'data-date="(\d{4}-\d{2}-\d{2})"', tag)
        if not d:
            continue
        i = re.search(r'\bid="([^"]+)"', tag)
        lv = re.search(r'data-level="(\d)"', tag)
        cnt = tips.get(i.group(1), 0) if i else 0
        days[d.group(1)] = (cnt, int(lv.group(1)) if lv else 0)
    if len(days) < 300:
        raise RuntimeError(f"contribution calendar looks incomplete ({len(days)} days)")
    return dict(sorted(days.items()))


def norm_api(items):
    out = []
    for r in items:
        if r.get("private"):
            continue
        out.append(dict(name=r["name"], lang=r.get("language"), upd=(r.get("pushed_at") or r.get("updated_at") or "")[:10],
                        desc=r.get("description") or ""))
    return out


def scrape_repos():
    out, seen = [], set()
    for page in range(1, 8):
        t = get_page(f"https://github.com/{USER}?tab=repositories&page={page}", f"repos{page}.html" if page > 1 else "repos.html")
        parts = re.split(r'(?=itemprop="name codeRepository")', t)[1:]
        new = 0
        for b in parts:
            n = re.search(r'itemprop="name codeRepository"[^>]*>\s*([^<]+?)\s*<', b)
            if not n or n.group(1) in seen:
                continue
            seen.add(n.group(1)); new += 1
            l = re.search(r'itemprop="programmingLanguage">([^<]+)<', b)
            u = re.search(r'<relative-time[^>]*datetime="([^"]+)"', b)
            d = re.search(r'itemprop="description"[^>]*>\s*(.*?)\s*</p>', b, re.S)
            desc = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html.unescape(d.group(1)))) if d else ""
            out.append(dict(name=n.group(1), lang=l.group(1) if l else None, upd=u.group(1)[:10] if u else "", desc=desc))
        if new == 0:
            break
    return out


def fetch_repos():
    if not OFFLINE:
        tok = os.environ.get("GITHUB_TOKEN")
        try:
            out, page = [], 1
            while page < 8:
                data = json.loads(http_get(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}&type=owner",
                                           accept="application/vnd.github+json", token=tok))
                if not isinstance(data, list) or not data:
                    break
                out += norm_api(data); page += 1
                if len(data) < 100:
                    break
            if out:
                return out
        except Exception as e:  # rate limit or network: fall back to scraping
            print("API failed, scraping instead:", e, file=sys.stderr)
    out = scrape_repos()
    if not out:
        raise RuntimeError("no repositories found")
    return out

# ───────────────────────── analysis ─────────────────────────
def d2(s): return dt.date.fromisoformat(s)

def analyse(days):
    ds = list(days)
    counts = {d: days[d][0] for d in ds}
    total = sum(counts.values())
    ranges, s, prev = [], None, None
    for d in ds:
        if counts[d] > 0:
            if s is None:
                s = d
            prev = d
        elif s is not None:
            ranges.append((s, prev, (d2(prev) - d2(s)).days + 1)); s = None
    if s is not None:
        ranges.append((s, prev, (d2(prev) - d2(s)).days + 1))
    longest = max(ranges, key=lambda r: r[2]) if ranges else None
    last = ds[-1]
    end = last if counts[last] > 0 else (ds[-2] if len(ds) > 1 else last)
    cur = next((r for r in ranges if r[1] == end), None)
    best_day = max(ds, key=lambda d: counts[d])
    months, wk = {}, [0] * 7
    for d in ds:
        k = d[:7]
        months[k] = months.get(k, 0) + counts[d]
        wk[(d2(d).weekday() + 1) % 7] += counts[d]
    return dict(total=total, longest=longest, current=cur, best_day=(best_day, counts[best_day]),
                months=months, weekday=wk, first=ds[0], last=last, counts=counts)

# ───────────────────────── svg helpers ─────────────────────────
W = 1024
L0, R0 = 33, 995           # left / right rule
BG, ORG, BONE, GRY, DIM, LINE = "#0A0A0A", "#FF5B0F", "#EDE9E2", "#8B8B8B", "#3A3A3A", "#303030"
HEAT = ["#262626", "#5B2A12", "#93400F", "#D4560F", "#FF6A14"]
MONO = "'JetBrains Mono','SF Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
DISP = "'Arial Black','Helvetica Neue','Inter',Arial,sans-serif"
P = 24
SPL = "0.2 0.0 0.0 1"
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def esc(s): return html.escape(str(s), quote=False)
def mdate(d): return f"{MON[int(d[5:7]) - 1]} {int(d[8:10])}" if d else ""
def mdate_y(d): return f"{MON[int(d[5:7]) - 1]} {int(d[8:10])}, {d[:4]}"
def kt(pts, per): return ";".join(f"{t / per:.4f}" for t, _ in pts)
def vv(pts): return ";".join(str(v) for _, v in pts)


def aloop(attr, pts, per=P, ease=True):
    sp = f' calcMode="spline" keySplines="{";".join([SPL] * (len(pts) - 1))}"' if ease else ""
    return f'<animate attributeName="{attr}" dur="{per}s" repeatCount="indefinite" keyTimes="{kt(pts, per)}" values="{vv(pts)}"{sp}/>'


def reveal(inner, b, per=P, dy=8):
    tr = (f'<animateTransform attributeName="transform" type="translate" dur="{per}s" repeatCount="indefinite" '
          f'keyTimes="{kt([(0, 0), (b, 0), (b + .6, 0), (per, 0)], per)}" values="0 {dy};0 {dy};0 0;0 0" calcMode="spline" '
          f'keySplines="{";".join([SPL] * 3)}"/>')
    return f'<g opacity="0">{aloop("opacity", [(0, 0), (b, 0), (b + .6, 1), (per - 1, 1), (per, 0)], per)}{tr}{inner}</g>'


def once(inner, b, dy=8, d=.7):
    return (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{b}s" dur="{d}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" begin="{b}s" dur="{d}s" fill="freeze" '
            f'calcMode="spline" keySplines="{SPL}" keyTimes="0;1"/>{inner}</g>')


def tx(x, y, s, size=13, fill=BONE, w=400, anchor="start", ls=0, disp=False, extra=""):
    fam = DISP if disp else MONO
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{w}" fill="{fill}"{a}{l} {extra}>{s}</text>'


def cap(x, y, s, fill=GRY, anchor="start", size=10.5):
    return tx(x, y, esc(s.upper()), size, fill, 500, anchor, 1.6)


def hl(y, x1=L0, x2=R0, c=LINE): return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{c}" stroke-width="1"/>'
def vl(x, y1, y2, c=LINE): return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{c}" stroke-width="1"/>'


def icon(name, x, y, s=18, c=ORG, sw=1.7):
    paths = {
        "pin": '<path d="M12 22s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="10" r="2.6"/>',
        "layers": '<path d="M12 3 2 8l10 5 10-5-10-5z"/><path d="M2 13l10 5 10-5"/><path d="M2 17.5l10 5 10-5"/>',
        "pulse": '<path d="M2 12h4l2.2-6 4 12 3-9 1.8 3H22"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.4 2"/>',
        "ext": '<path d="M14 4h6v6"/><path d="M20 4 10.5 13.5"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
        "flame": '<path d="M12 22c-4 0-7-2.8-7-6.8 0-3 2-4.7 3.2-6.7.7-1.1 1-2.3.9-3.5 2.7 1.4 4.3 3.7 4.5 6 .8-.6 1.3-1.6 1.4-2.8 2.2 2 3.1 4.4 3.1 6.9 0 4-3 6.9-6 6.9z"/><path d="M12 22c-1.8 0-3-1.2-3-2.9 0-1.6 1.2-2.4 2-3.8.6.9 2.2 1.6 3 2.9.4 2-.6 3.8-2 3.8z"/>',
    }
    return f'<g transform="translate({x},{y}) scale({s / 24})" fill="none" stroke="{c}" stroke-width="{sw * 24 / s:.2f}" stroke-linecap="round" stroke-linejoin="round">{paths[name]}</g>'


GH = "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"


def ghmark(x, y, s=20, c=BONE):
    return f'<g transform="translate({x},{y}) scale({s / 24})"><path d="{GH}" fill="{c}"/></g>'


def corner(x, y, sx, sy, size=26):
    return f'<path d="M{x},{y + sy * size} V{y} H{x + sx * size}" fill="none" stroke="{ORG}" stroke-width="2"><animate attributeName="opacity" values="1;.35;1" dur="3s" repeatCount="indefinite"/></path>'

# ───────────────────────── render ─────────────────────────
def render(days, repos):
    st = analyse(days)
    body, defs = [], []
    uid = [0]

    def nid(p):
        uid[0] += 1
        return f"{p}{uid[0]}"

    def hdr(y, title, right=""):
        s = tx(34, y, "»", 20, ORG, 700) + tx(60, y, esc(title.upper()), 17, BONE, 700, ls=1.6) + hl(y + 14)
        if right:
            s += cap(R0, y - 2, right, GRY, "end", 11)
        return s

    byname = {r["name"]: r for r in repos}
    nrep = len(repos)
    ntS = sum(r["lang"] == "TypeScript" for r in repos)
    ntJ = sum(r["lang"] == "JavaScript" for r in repos)
    nOth = nrep - ntS - ntJ
    today = dt.date.today().isoformat()
    cur, lon = st["current"], st["longest"]

    # background grid
    defs.append(f'<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>')

    # ── top bar ──
    body.append(tx(35, 31, "&gt;", 18, ORG, 700) + tx(60, 31, "ALMOSTALOK", 16, BONE, 500, ls=1.5) + tx(216, 31, "/", 16, GRY) + tx(254, 31, "SYSTEM PROFILE", 15, "#C9C4BB", 400, ls=1.5)
                + tx(420, 31, "/", 16, GRY) + tx(462, 31, "INDIA", 15, "#C9C4BB", 400, ls=1.5)
                + tx(868, 31, "[", 17, GRY) + tx(893, 31, "README.MD", 14.5, ORG, 500, ls=1.2) + tx(982, 31, "]", 17, GRY) + hl(49))
    # left rail
    body.append(tx(32, 82, "+", 16, GRY, anchor="middle") + vl(60, 150, 500, "#2a2a2a"))
    for i, n in enumerate(["01", "02", "03"]):
        body.append(tx(24, 172 + i * 33, n, 15, ORG if i == 2 else GRY, 500 if i == 2 else 400))
    body.append(f'<rect x="24" y="270" width="12" height="2" fill="{ORG}"/>')
    # name (two stacked lines: ALMOST / ALOK.)
    body.append(once(f'<text x="86" y="182" font-family="{DISP}" font-size="98" font-weight="900" fill="{BONE}" textLength="410" lengthAdjust="spacingAndGlyphs">ALMOST</text>', .1, 12, .9))
    body.append(once(f'<text x="86" y="276" font-family="{DISP}" font-size="98" font-weight="900" fill="{ORG}" textLength="318" lengthAdjust="spacingAndGlyphs">ALOK.</text>', .3, 12, .9))
    body.append(once(tx(90, 328, "//", 21, ORG, 500) + tx(130, 328, "DEVELOPER &amp; PRODUCT BUILDER", 17, BONE, 400, ls=3), .6))
    body.append(once(tx(91, 361, "Useful products for real people &#8212;", 15.5, BONE) + tx(91, 383, "from first idea to shipped. Ship &gt; Perfection.", 15.5, BONE)
                     + f'<rect x="{91 + 47 * 9.3 + 6:.0f}" y="368" width="3" height="16" fill="{ORG}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>', .9))
    # badge
    bx, by_, bw, bh = 88, 417, 358, 72
    body.append(once(f'<path d="M{bx},{by_} H{bx + bw - 14} L{bx + bw},{by_ + 14} V{by_ + bh - 14} L{bx + bw - 14},{by_ + bh} H{bx} Z" fill="none" stroke="{ORG}" stroke-width="1.5"/>'
                     + f'<path d="M{bx + 19},{by_ + 20} V{by_ + 12} H{bx + 27} M{bx + 59},{by_ + 12} H{bx + 67} V{by_ + 20} M{bx + 67},{by_ + 52} V{by_ + 60} H{bx + 59} M{bx + 27},{by_ + 60} H{bx + 19} V{by_ + 52}" fill="none" stroke="{ORG}" stroke-width="2"/>'
                     + tx(bx + 43, by_ + 48, "H", 36, ORG, 900, "middle", disp=True)
                     + tx(bx + 82, by_ + 33, f'BUILDING <tspan fill="{ORG}" font-weight="700">HOSPATE</tspan>', 20, BONE, 500, ls=1.2)
                     + tx(bx + 82, by_ + 57, "HOSPITAL ERP", 14.5, GRY, 400, ls=1.6), 1.1))
    # ascii portrait
    rows = [r for r in open(PORTRAIT, encoding="utf-8").read().split("\n")]
    rows = (rows + [""] * 41)[:41]
    COLS = 78
    cw, lh, fs = 5.9, 7.95, 9.8
    AW, AH = COLS * cw, 41 * lh
    HP = 20
    rows = [r.ljust(COLS) for r in rows]
    glyphs = sum(1 for r in rows for c in r if c != " ")

    def arows(strs, fill):
        return "".join(f'<text x="0" y="{i * lh + lh * .82:.1f}" font-family="{MONO}" font-size="{fs}" fill="{fill}" textLength="{AW:.1f}" lengthAdjust="spacing" xml:space="preserve">{esc(s)}</text>'
                       for i, s in enumerate(strs) if s.strip())
    rnd = random.Random(11)
    noise = ["".join(rnd.choice("@#%*+=-:.01/<>{}") for _ in range(COLS)) for _ in range(41)]
    defs.append(f'<g id="art">{arows(rows, BONE)}</g><g id="artA">{arows(rows, ORG)}</g>')
    defs.append(f'<mask id="mW" maskUnits="userSpaceOnUse" x="0" y="0" width="{AW:.0f}" height="{AH:.0f}"><rect width="{AW:.0f}" height="0" fill="#fff">{aloop("height", [(0, 0), (4, AH), (HP, AH)], HP, False)}</rect></mask>'
                f'<mask id="mN" maskUnits="userSpaceOnUse" x="0" y="0" width="{AW:.0f}" height="{AH:.0f}"><rect width="{AW:.0f}" height="{AH:.0f}" fill="#fff">{aloop("y", [(0, 0), (4, AH), (HP, AH)], HP, False)}{aloop("height", [(0, AH), (4, 0), (HP, 0)], HP, False)}</rect></mask>'
                f'<mask id="mS" maskUnits="userSpaceOnUse" x="0" y="0" width="{AW:.0f}" height="{AH:.0f}"><rect width="{AW:.0f}" height="22" y="-22" fill="#fff">{aloop("y", [(0, -22), (5, -22), (9.5, AH), (HP, AH)], HP, False)}</rect></mask>')
    ax, ay = 524, 140
    body.append(f'<g transform="translate({ax},{ay})"><g mask="url(#mN)" opacity=".55">{arows(noise, "#4A4A4A")}</g>'
                f'<g>{aloop("opacity", [(0, 1), (HP - 1.4, 1), (HP - .3, 0), (HP, 0)], HP, False)}<use href="#art" mask="url(#mW)"/><use href="#artA" mask="url(#mS)"/></g></g>')
    body.append(corner(ax - 14, 92, 1, 1) + corner(R0 - 4, 92, -1, 1) + corner(R0 - 14, 496, -1, -1))
    body.append(cap(ax, ay + AH + 30, f"portrait.asc · {COLS}x41 · {glyphs:,} glyphs · regen {HP}s", "#5E5E5E", size=9.5))

    # ── stats strip ──
    sy = 540
    body.append(hl(sy) + hl(sy + 72))
    rnd2 = random.Random(5); bx_ = 36; bars = ""
    while bx_ < 104:
        w = rnd2.choice([1, 1, 2, 3]); bars += f'<rect x="{bx_}" y="{sy + 14}" width="{w}" height="40" fill="{BONE}" opacity=".9"/>'; bx_ += w + rnd2.choice([2, 2, 3])
    body.append(bars + vl(135, sy + 14, sy + 58))
    cells = [("Status", "&gt; BUILDING", ORG, None), ("Focus", "PRODUCT / DEV", BONE, None), ("Location", "INDIA", BONE, "pin"),
             ("Stack", "FULL-STACK", BONE, "layers"), ("Repos", f"{nrep} PUBLIC", BONE, "pulse")]
    xs = [172, 335, 500, 660, 830]
    for (a, v, c, ic), x in zip(cells, xs):
        body.append(cap(x, sy + 24, a, GRY, size=10.5))
        if ic:
            body.append(icon(ic, x - 1, sy + 33, 19, BONE, 1.5) + tx(x + 28, sy + 49, v, 15, c, 500, ls=1.5))
        else:
            body.append(tx(x, sy + 49, v, 15, c, 500, ls=1.5))
    for x in (305, 480, 640, 800):
        body.append(vl(x, sy + 14, sy + 58))

    # ── contributions ──
    cy0 = 648
    body.append(hdr(cy0, "GitHub contributions", "Last 365 days"))
    ds = list(days)
    first = d2(ds[0])
    pitch, cell = 13.4, 10.6
    gx, gy = 67, cy0 + 50
    cells_svg, mlbl, seen_m, ncol = "", "", set(), 0
    for d in ds:
        dd = d2(d); col = (dd - first).days // 7; row = (dd.weekday() + 1) % 7
        ncol = max(ncol, col + 1)
        cnt, lv = days[d]
        cells_svg += f'<rect x="{gx + col * pitch:.1f}" y="{gy + row * pitch:.1f}" width="{cell}" height="{cell}" fill="{HEAT[lv]}"/>'
        if dd.day <= 7 and row == 0 and d[:7] not in seen_m:
            seen_m.add(d[:7]); mlbl += cap(gx + col * pitch, gy - 14, MON[dd.month - 1], "#B5B0A7", size=10.5)
    lastd = d2(ds[-1]); lc = (lastd - first).days // 7; lr = (lastd.weekday() + 1) % 7
    cells_svg += f'<rect x="{gx + lc * pitch - 1.5:.1f}" y="{gy + lr * pitch - 1.5:.1f}" width="{cell + 3}" height="{cell + 3}" fill="none" stroke="{BONE}" stroke-width="1.2"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></rect>'
    gw = ncol * pitch
    cid = nid("hm")
    defs.append(f'<clipPath id="{cid}"><rect x="{gx - 2}" y="{gy - 24}" width="0" height="{pitch * 7 + 28}">{aloop("width", [(0, 0), (.3, 0), (3.2, gw + 4), (P, gw + 4)], P)}</rect></clipPath>')
    leg = cap(gx + 560, gy + 7 * pitch + 18, "Less", GRY, "end", 9.5) + "".join(f'<rect x="{gx + 568 + i * 15}" y="{gy + 7 * pitch + 9}" width="10.6" height="10.6" fill="{HEAT[i]}"/>' for i in range(5)) + cap(gx + 568 + 5 * 15 + 4, gy + 7 * pitch + 18, "More", GRY, size=9.5)
    body.append(reveal(mlbl + f'<g clip-path="url(#{cid})">{cells_svg}</g>' + leg, .1))
    px = 811
    body.append(vl(px, gy - 26, gy + 7 * pitch + 12))
    flame = f'<g><animateTransform attributeName="transform" type="scale" additive="sum" values="1 1;1.04 .97;1 1" dur="1.4s" repeatCount="indefinite"/></g>'
    body.append(f'<g>{icon("flame", 838, gy + 4, 36, ORG, 1.6)}</g>' + tx(884, gy + 38, str(cur[2] if cur else 0), 46, ORG, 700, disp=True)
                + tx(839, gy + 62, "DAY STREAK", 15, BONE, 500, ls=2.4)
                + tx(839, gy + 83, f"BEST {lon[2] if lon else 0} DAYS", 12, ORG, 500, ls=1.5)
                + tx(839, gy + 103, f"{st['total']:,} contributions", 12.5, "#CFC9BF") + tx(839, gy + 120, "in the last year", 12.5, "#CFC9BF"))
    y = gy + 7 * pitch + 50

    # ── telemetry ──
    body.append(hdr(y + 18, "Telemetry", "Live from GitHub"))
    ty = y + 56
    colw = (R0 - L0) / 4
    # by month
    mk = sorted(st["months"])[-12:]
    mx = max(st["months"][k] for k in mk) or 1
    bh_ = 90; base = ty + 22 + bh_
    mc = cap(L0 + 4, ty, "By month")
    for i, k in enumerate(mk):
        v = st["months"][k]; h = max(2, v / mx * bh_); x = L0 + 6 + i * 18.4; isl = i == len(mk) - 1; b = .3 + i * .07
        mc += (f'<rect x="{x:.1f}" y="{base - h:.1f}" width="12" height="{h:.1f}" fill="{ORG if isl else "#CFC9BF"}">{aloop("height", [(0, 0), (b, 0), (b + 1, h), (P, h)], P)}{aloop("y", [(0, base), (b, base), (b + 1, base - h), (P, base - h)], P)}</rect>'
               + tx(x + 6, base + 14, MON[int(k[5:]) - 1][0], 9.5, GRY, anchor="middle"))
        if v == max(st["months"][kk] for kk in mk) or isl:
            mc += tx(x + 6, base - h - 5, str(v), 9.5, BONE, anchor="middle")
    mc += hl(base, L0 + 4, L0 + colw - 20)
    body.append(reveal(mc, .2))
    # weekday
    wx = L0 + colw + 16
    wk = st["weekday"]; wmx = max(wk) or 1
    wc = cap(wx, ty, "By weekday")
    for i, n in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
        yy = ty + 20 + i * 15; ln = max(2, wk[i] / wmx * 150)
        wc += cap(wx, yy + 9, n, GRY, size=9.5) + f'<rect x="{wx + 34}" y="{yy}" width="0" height="9" fill="{ORG if wk[i] == wmx else "#CFC9BF"}"><animate attributeName="width" dur="{P}s" repeatCount="indefinite" keyTimes="{kt([(0, 0), (.6, 0), (1.8, ln), (P, ln)], P)}" values="0;0;{ln:.1f};{ln:.1f}" calcMode="spline" keySplines="{";".join([SPL] * 3)}"/></rect>' + tx(wx + 40 + ln, yy + 8.5, str(wk[i]), 9.5, BONE)
    body.append(vl(L0 + colw, ty - 14, ty + 124) + reveal(wc, .4))
    # language mix
    lx = L0 + 2 * colw + 16
    lc_ = cap(lx, ty, "Language mix") + tx(lx, ty + 50, str(nrep), 40, BONE, 700, disp=True) + tx(lx + 76, ty + 50, "repos", 12, GRY)
    xx = lx; wtot = colw - 40
    for nm, cnt, col in [("TypeScript", ntS, ORG), ("JavaScript", ntJ, "#CFC9BF"), ("Other", nOth, "#555")]:
        if cnt:
            w = wtot * cnt / nrep; lc_ += f'<rect x="{xx:.1f}" y="{ty + 68}" width="{max(w - 2, 2):.1f}" height="10" fill="{col}"/>'; xx += w
    ly = ty + 100
    for nm, cnt, col in [("TypeScript", ntS, ORG), ("JavaScript", ntJ, "#CFC9BF"), ("Other", nOth, "#555")]:
        if cnt:
            lc_ += f'<rect x="{lx}" y="{ly - 8}" width="8" height="8" fill="{col}"/>' + tx(lx + 14, ly, f'{nm} <tspan fill="{BONE}">{cnt}</tspan>', 11, GRY); ly += 16
    body.append(vl(L0 + 2 * colw, ty - 14, ty + 124) + reveal(lc_, .6))
    # pushes by month
    pm = {}
    for r in repos:
        if r["upd"]:
            pm[r["upd"][:7]] = pm.get(r["upd"][:7], 0) + 1
    keys = sorted(pm)[-9:]
    pmx = max(pm[k] for k in keys) or 1
    px_ = L0 + 3 * colw + 16
    pc = cap(px_, ty, "Last pushed")
    base2 = ty + 22 + 78
    for i, k in enumerate(keys):
        v = pm[k]; h = max(2, v / pmx * 78); x = px_ + i * 25; b = .3 + i * .07
        pc += (f'<rect x="{x}" y="{base2 - h:.1f}" width="14" height="{h:.1f}" fill="#CFC9BF">{aloop("height", [(0, 0), (b, 0), (b + 1, h), (P, h)], P)}{aloop("y", [(0, base2), (b, base2), (b + 1, base2 - h), (P, base2 - h)], P)}</rect>'
               + tx(x + 7, base2 - h - 5, str(v), 9.5, BONE, anchor="middle") + tx(x + 7, base2 + 14, MON[int(k[5:]) - 1][0], 9.5, GRY, anchor="middle"))
    pc += hl(base2, px_, R0 - 10)
    body.append(vl(L0 + 3 * colw, ty - 14, ty + 124) + reveal(pc, .8))
    y = ty + 168

    # ── repositories ──
    body.append(hdr(y + 18, "Featured repositories", f"{len(FEATURED)} / {nrep}"))
    ry0 = y + 40
    RH = 86
    feat_names = set()
    for i, (rn, title, desc) in enumerate(FEATURED):
        r = byname.get(rn, {}); feat_names.add(rn)
        yy = ry0 + i * RH
        dl_ = textwrap.wrap(desc, 56)[:2]
        row = f'<rect x="34" y="{yy + 14}" width="3" height="52" fill="{ORG}"/>' + tx(58, yy + 46, f"[{i + 1:02d}]", 17, BONE, 400)
        row += tx(126, yy + 30, esc(title.upper()), 19, ORG, 700, ls=1) + "".join(tx(126, yy + 51 + j * 17, esc(l), 12.5, "#CFC9BF") for j, l in enumerate(dl_))
        row += ghmark(594, yy + 14, 17, BONE) + f'<rect x="619" y="{yy + 12}" width="66" height="21" rx="3" fill="none" stroke="{GRY}"/>' + cap(652, yy + 27, "PUBLIC", BONE, "middle", 9.5)
        row += tx(594, yy + 58, f'{esc(r.get("lang") or "—")}   <tspan fill="{GRY}">·</tspan>   pushed {mdate(r.get("upd", ""))}', 12.5, "#CFC9BF")
        row += vl(892, yy + 22, yy + 62) + icon("clock", 910, yy + 26, 18, BONE, 1.6) + tx(936, yy + 40, esc(mdate(r.get("upd", "")).upper()), 14, BONE, 500, ls=1)
        row += hl(yy + RH - 2, L0, R0, "#262626")
        body.append(reveal(row, .15 + i * .1))
    y = ry0 + len(FEATURED) * RH
    others = [r["name"] for r in sorted(repos, key=lambda r: r["upd"], reverse=True) if r["name"] not in feat_names and r["name"] not in SKIP_INDEX]
    lines_, line = [], ""
    for n in others:
        nxt = (line + "  /  " if line else "") + n
        if len(nxt) * 7.0 > R0 - 60 - 60 and line:
            lines_.append(line); line = n
        else:
            line = nxt
    if line:
        lines_.append(line)
    ix = cap(58, y + 22, f"+ {len(others)} more repositories", ORG, size=11)
    for j, l in enumerate(lines_):
        ix += tx(58, y + 46 + j * 20, esc(l), 11.5, "#9A958C")
    body.append(reveal(ix, .4))
    y = y + 46 + len(lines_) * 20 + 30

    # ── tech stack ──
    body.append(hdr(y + 18, "Tech stack"))
    body.append(tx(62, y + 52, "$", 15, ORG, 700) + tx(82, y + 52, "cat stack.txt", 15, BONE))
    bx0, bx1 = 35, R0 - 1
    bt = y + 66
    colw2 = (bx1 - bx0) / 5
    wr = []
    for g, items in STACK:
        wr.append((g, textwrap.wrap(", ".join(items), 20)))
    hmax = max(len(l) for _, l in wr)
    bh2 = 46 + hmax * 18
    body.append(f'<rect x="{bx0}" y="{bt}" width="{bx1 - bx0}" height="{bh2}" rx="5" fill="none" stroke="{LINE}"/>')
    sk = ""
    for i, (g, lns) in enumerate(wr):
        x = bx0 + i * colw2 + 22
        if i:
            sk += vl(bx0 + i * colw2, bt + 12, bt + bh2 - 12)
        sk += tx(x, bt + 28, esc(g.replace(" / ", " / ")), 13.5, ORG, 700)
        for j, l in enumerate(lns):
            sk += tx(x, bt + 52 + j * 18, (f'<tspan fill="{ORG}">&gt;</tspan> ' if j == 0 else "&#160;&#160;") + esc(l), 12, BONE)
    body.append(reveal(sk, .2))
    y = bt + bh2 + 30

    # ── terminal ──
    body.append(hdr(y + 18, "Terminal"))
    wt = y + 40
    lines = [("cmd", "npx almostalok"), ("out", [("&#9492;&#9472; ", GRY), ("about", BONE)]),
             ("out", [("   &#9500;&#9472; ", GRY), ("name: ", GRY), ("almostalok (Alok Kumar Singh)", BONE)]),
             ("out", [("   &#9500;&#9472; ", GRY), ("role: ", GRY), ("Developer &amp; Product Builder", BONE)]),
             ("out", [("   &#9500;&#9472; ", GRY), ("building: ", GRY), ("Hospate (hospital ERP)", BONE)]),
             ("out", [("   &#9500;&#9472; ", GRY), ("location: ", GRY), ("India", BONE)]),
             ("out", [("   &#9500;&#9472; ", GRY), ("philosophy: ", GRY), ("Ship &gt; Perfection", BONE)]),
             ("out", [("   &#9492;&#9472; ", GRY), ("status: ", GRY), ("Building...", BONE)])]
    LHt = 22
    TH = 64 + len(lines) * LHt + 26
    body.append(f'<rect x="36" y="{wt}" width="{R0 - 38}" height="{TH}" rx="14" fill="#0C0C0C" stroke="#3A3A3A" stroke-width="1.2"/>'
                f'<circle cx="58" cy="{wt + 24}" r="6" fill="#FF5F57"/><circle cx="78" cy="{wt + 24}" r="6" fill="#FEBC2E"/><circle cx="98" cy="{wt + 24}" r="6" fill="#28C840"/>'
                f'<path d="M118,{wt + 34} V{wt + 20} Q118,{wt + 12} 126,{wt + 12} H{R0 - 120} Q{R0 - 112},{wt + 12} {R0 - 112},{wt + 20} V{wt + 34}" fill="none" stroke="#3A3A3A"/>'
                f'<text x="148" y="{wt + 29}" font-family="{MONO}" font-size="13" fill="{BONE}">almostalok@dev: ~</text>'
                f'<path d="M{R0 - 62},{wt + 24} h12" stroke="{GRY}" stroke-width="1.4"/><rect x="{R0 - 34}" y="{wt + 18}" width="12" height="12" rx="2" fill="none" stroke="{GRY}" stroke-width="1.4"/>'
                f'<line x1="37" y1="{wt + 40}" x2="{R0 - 1}" y2="{wt + 40}" stroke="#3A3A3A"/>')
    inner, tcur, PX = "", .8, 58
    CWt = 8.5
    for i, (kind, content) in enumerate(lines):
        yy = wt + 48 + (i + 1) * LHt + 4
        if kind == "cmd":
            segs_ = [("$ ", ORG), ("npx ", ORG), (content.replace("npx ", ""), BONE)]; d = len(content) * .05
        else:
            segs_, d = content, .22
        w = sum(len(s.replace("&#9492;", "x").replace("&#9500;", "x").replace("&#9472;", "x").replace("&gt;", ">").replace("&amp;", "&").replace("&#160;", " ")) for s, _ in segs_) * CWt + 8
        cid = nid("t")
        defs.append(f'<clipPath id="{cid}"><rect x="{PX - 2}" y="{yy - 17}" width="0" height="24">{aloop("width", [(0, 0), (tcur, 0), (tcur + d, w), (P, w)], P, False)}</rect></clipPath>')
        spans = "".join(f'<tspan fill="{c}">{s}</tspan>' for s, c in segs_)
        inner += f'<text x="{PX}" y="{yy}" font-family="{MONO}" font-size="14" xml:space="preserve" clip-path="url(#{cid})">{spans}</text>'
        if i == len(lines) - 1:
            inner += (f'<g opacity="0">{aloop("opacity", [(0, 0), (tcur + d, 0), (tcur + d + .01, 1), (P, 1)], P, False)}'
                      f'<rect x="{PX + w + 2:.1f}" y="{yy - 14}" width="10" height="17" fill="{ORG}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect></g>')
        tcur += d + (.4 if kind == "cmd" else .12)
    body.append(inner)
    y = wt + TH + 36

    # ── connect ──
    body.append(hl(y) + tx(34, y + 44, "»", 20, ORG, 700) + tx(60, y + 44, "CONNECT", 16, ORG, 700, ls=1.8))
    c1 = ghmark(188, y + 26, 24, BONE) + tx(230, y + 43, "github.com/almostalok", 13.5, BONE)
    c2 = tx(484, y + 46, "in", 25, BONE, 800, disp=True) + tx(524, y + 43, "linkedin.com/in/alokkumarsingh", 13.5, BONE)
    c3 = icon("ext", 812, y + 25, 22, BONE, 1.7) + tx(850, y + 43, "almostalok.tech", 13.5, BONE)
    body.append(c1 + c2 + c3 + vl(455, y + 22, y + 56) + vl(790, y + 22, y + 56))
    y2 = y + 84
    more = [("blog", "almostalokblogs.tech"), ("resume", "almostalokresume.tech"), ("x", "@almostalok"), ("instagram", "@almostalok"), ("youtube", "/c/almostalok")]
    for i, (k, v) in enumerate(more):
        body.append(cap(60 + i * 186, y2, k, GRY, size=9.5) + tx(60 + i * 186, y2 + 18, esc(v), 12, "#CFC9BF"))
    y2 += 24
    body.append(hl(y2 + 24, L0, R0, "#262626") + cap(L0 + 2, y2 + 46, f"built {today} from live github data", "#555", size=9.5) + cap(R0, y2 + 46, "> almostalok // end of process", "#555", "end", 9.5))
    H = y2 + 66

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="almostalok, system profile. Developer and product builder from India, building Hospate. Live ASCII portrait, GitHub contributions and streak, telemetry, featured repositories, tech stack, terminal and links.">\n'
           f'<defs>{"".join(defs)}</defs>\n<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#grid)"/>\n{"".join(body)}\n</svg>')
    return svg, dict(H=H, total=st["total"], cur=cur, lon=lon, repos=nrep, ts=ntS, js=ntJ)


def main():
    days = fetch_contributions()
    repos = fetch_repos()
    svg, info = render(days, repos)
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", OUT, info)


if __name__ == "__main__":
    main()
