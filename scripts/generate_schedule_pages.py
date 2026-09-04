#!/usr/bin/env python3
"""Generate static ship-schedule hub, year and month pages for St Kitts.

St Kitts uses hand-authored HTML with /css/styles.css and /js/main.js
(not the Cozumel/Aruba partials + Tailwind + site.js shell).

CONFIG-DRIVEN: reads scripts/destination.config.json.
GENERATED FROM CARIBBEAN AUTHORITY - DO NOT MANUALLY EDIT schedule HTML by hand.
Run: node scripts/sync-schedules.mjs && python3 scripts/generate_schedule_pages.py
"""
from __future__ import annotations

import json
from calendar import month_name
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "scripts" / "destination.config.json").read_text(encoding="utf-8"))

DOMAIN = CONFIG["domain"]
SITE = CONFIG["siteName"]
HUB = CONFIG.get("scheduleHubPath", "ship-schedule")
DATA = ROOT / CONFIG["localOutput"]
DEST = CONFIG["destinationName"]
PORT_GUIDE = CONFIG["portGuidePath"]
BEST_EXCURSIONS = CONFIG["bestExcursionsPath"]
ONE_DAY = CONFIG["oneDayPath"]
HUB_INTRO = CONFIG.get(
    "hubIntro",
    f"Find your ship and date for {DEST}, then plan a realistic port day.",
)

# Editorial + legal URLs preserved/added in sitemap (schedule entries appended).
EDITORIAL_SITEMAP: list[tuple[str, str, str]] = [
    ("", "1.0", "weekly"),
    ("excursions.html", "0.9", "weekly"),
    ("port-guide.html", "0.8", "monthly"),
    ("one-day-in-st-kitts.html", "0.8", "monthly"),
    ("private-tours.html", "0.8", "monthly"),
    ("railway-tours.html", "0.8", "monthly"),
    ("faq.html", "0.7", "monthly"),
    ("contact.html", "0.5", "yearly"),
    ("st-kitts-scenic-railway-tour.html", "0.9", "monthly"),
    ("brimstone-hill-fortress-tour.html", "0.9", "monthly"),
    ("island-highlights-tour.html", "0.9", "monthly"),
    ("south-east-peninsula-tour.html", "0.9", "monthly"),
    ("catamaran-snorkel-cruise.html", "0.9", "monthly"),
    ("rainforest-and-monkey-tour.html", "0.8", "monthly"),
    ("private-st-kitts-tour.html", "0.9", "monthly"),
    ("beach-and-sightseeing-tour.html", "0.9", "monthly"),
    ("island-tour-vs-beach.html", "0.8", "monthly"),
    ("st-kitts-vs-nevis.html", "0.7", "monthly"),
    ("about.html", "0.5", "yearly"),
    ("privacy.html", "0.3", "yearly"),
    ("terms.html", "0.3", "yearly"),
    ("methodology.html", "0.5", "yearly"),
]


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def nav_html(current: str = "") -> str:
    items = [
        ("/", "Home", "home"),
        ("/excursions.html", "Excursions", "excursions"),
        ("/railway-tours.html", "Railway Tours", "railway"),
        ("/private-tours.html", "Private Tours", "private"),
        (f"/{HUB}/", "Ship Schedule", "schedule"),
        ("/port-guide.html", "Port Guide", "port"),
        ("/one-day-in-st-kitts.html", "One Day", "oneday"),
        ("/faq.html", "FAQ", "faq"),
        ("/contact.html", "Contact", "contact"),
    ]
    lis = []
    for href, label, key in items:
        cur = ' aria-current="page"' if key == current else ""
        lis.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f"""  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="logo" aria-label="St Kitts Shore Excursions home">
        <span class="logo-icon" aria-hidden="true">&#9733;</span>
        <span>St Kitts Shore<br>Excursions</span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Toggle navigation">&#9776;</button>
      <nav class="main-nav" id="main-nav" aria-label="Main navigation">
        <ul>
          {"".join(lis)}
        </ul>
      </nav>
    </div>
  </header>"""


def footer_html() -> str:
    return """  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="/" class="logo" style="color:#fff;">
            <span class="logo-icon" aria-hidden="true">&#9733;</span>
            <span>St Kitts Shore Excursions</span>
          </a>
          <p>Independent guide for cruise passengers comparing St Kitts shore excursions, cruise port tours and private island experiences. We do not operate tours directly.</p>
        </div>
        <div>
          <h3>Excursions</h3>
          <ul>
            <li><a href="/st-kitts-scenic-railway-tour.html">Scenic Railway</a></li>
            <li><a href="/brimstone-hill-fortress-tour.html">Brimstone Hill</a></li>
            <li><a href="/island-highlights-tour.html">Island Highlights</a></li>
            <li><a href="/catamaran-snorkel-cruise.html">Catamaran Cruise</a></li>
            <li><a href="/private-st-kitts-tour.html">Private Tours</a></li>
          </ul>
        </div>
        <div>
          <h3>Planning</h3>
          <ul>
            <li><a href="/ship-schedule/">Ship Schedule</a></li>
            <li><a href="/port-guide.html">Port Guide</a></li>
            <li><a href="/one-day-in-st-kitts.html">One Day in St Kitts</a></li>
            <li><a href="/island-tour-vs-beach.html">Island Tour vs Beach</a></li>
            <li><a href="/faq.html">FAQ</a></li>
            <li><a href="/contact.html">Contact enquiry</a></li>
          </ul>
        </div>
        <div>
          <h3>Site</h3>
          <ul>
            <li><a href="/about.html">About</a></li>
            <li><a href="/methodology.html">Methodology</a></li>
            <li><a href="/privacy.html">Privacy</a></li>
            <li><a href="/terms.html">Terms</a></li>
            <li><a href="/excursions.html">All Excursions</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 stkittsshoreexcursion.com. Compare St Kitts shore excursion options. Always verify cruise ship times before booking.</p>
      </div>
    </div>
  </footer>"""


def page_shell(
    *,
    title: str,
    description: str,
    canonical_path: str,
    body_html: str,
    nav_current: str = "schedule",
) -> str:
    canon = f"{DOMAIN}/{canonical_path}" if canonical_path else f"{DOMAIN}/"
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canon}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="{DOMAIN}/images/hero-st-kitts.png">
  <meta property="og:site_name" content="{esc(SITE)}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/css/styles.css?v=4">
</head>
<body>
{nav_html(nav_current)}

  <main>
{body_html}
  </main>

{footer_html()}
  <script src="/js/main.js" defer></script>
  <script src="/js/schedule-search.js" defer></script>
</body>
</html>
"""


def disclaimer() -> str:
    return """<p class="schedule-disclaimer">
  Cruise schedules can change. Arrival and departure times are planning guides only.
  Confirm final timings with your cruise line before you travel.
</p>"""


def month_label(ym: str) -> str:
    y, m = ym.split("-")
    return f"{month_name[int(m)]} {y}"


def call_cards_html(calls: list[dict], *, searchable: bool = True) -> str:
    cards = []
    for c in calls:
        ship = esc(c["ship"])
        line = esc(c["cruiseLine"])
        date = esc(c["date"])
        arr = esc(c.get("arrival") or "-")
        dep = esc(c.get("departure") or "-")
        tip = esc(c.get("timeInPort") or "")
        tip_html = f'<span class="schedule-card__tip">{tip} in port</span>' if tip else ""
        search = esc(f"{c['date']} {c['ship']} {c['cruiseLine']}".lower())
        cards.append(
            f"""<article class="schedule-card" data-search="{search}">
  <div class="schedule-card__date">{date}</div>
  <h3 class="schedule-card__ship">{ship}</h3>
  <p class="schedule-card__line">{line}</p>
  <dl class="schedule-card__times">
    <div><dt>Arrive</dt><dd>{arr}</dd></div>
    <div><dt>Depart</dt><dd>{dep}</dd></div>
  </dl>
  {tip_html}
</article>"""
        )
    table_rows = []
    for c in calls:
        table_rows.append(
            f"""<tr class="schedule-row" data-search="{esc(f"{c['date']} {c['ship']} {c['cruiseLine']}".lower())}">
  <td>{esc(c['date'])}</td>
  <td>{esc(c['ship'])}</td>
  <td>{esc(c['cruiseLine'])}</td>
  <td>{esc(c.get('arrival') or '-')}</td>
  <td>{esc(c.get('departure') or '-')}</td>
</tr>"""
        )
    search_ui = ""
    if searchable:
        search_ui = """<div class="schedule-search" role="search">
  <label for="schedule-filter" class="sr-only">Search by ship or date</label>
  <input id="schedule-filter" type="search" class="schedule-search__input" placeholder="Search ship name or date (YYYY-MM-DD)" autocomplete="off">
  <p class="schedule-search__hint">Filter updates instantly. No booking on this site.</p>
</div>"""
    return f"""{search_ui}
<div class="schedule-cards" data-schedule-list>{"".join(cards)}</div>
<div class="schedule-table-wrap">
  <table class="schedule-table">
    <thead>
      <tr>
        <th>Date</th>
        <th>Ship</th>
        <th>Cruise line</th>
        <th>Arrival</th>
        <th>Departure</th>
      </tr>
    </thead>
    <tbody data-schedule-list>{"".join(table_rows)}</tbody>
  </table>
</div>
<p class="schedule-empty hidden" data-schedule-empty>No calls match that search.</p>
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


def hub_page(meta: dict, by_year: dict, months: list[str]) -> str:
    year_links = "".join(
        f'<a class="decision-chip" href="{y}/">{y} · {by_year.get(y, 0)} calls</a>'
        for y in sorted(by_year)
        if by_year[y] > 0 and y != "2028"
    )
    month_links = "".join(
        f'<li><a href="{ym[:4]}/{ym[5:]}/">{month_label(ym)} ({meta["integrity"]["byMonth"][ym]} calls)</a></li>'
        for ym in months
    )
    return f"""<!-- GENERATED FROM CARIBBEAN AUTHORITY - DO NOT MANUALLY EDIT -->
    <div class="page-hero page-hero--schedule">
      <div class="hero-bg" aria-hidden="true"></div>
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">Ship Schedule</li></ol></nav>
        <h1>{esc(DEST)} cruise ship schedule</h1>
        <p>{esc(HUB_INTRO)}</p>
      </div>
    </div>
    <section class="schedule-hub">
      <div class="container schedule-narrow">
        <p>This schedule is synced from the Caribbean Shore Excursions authority dataset for {esc(DEST)} only. It lists planned Port Zante calls so you can match railway, Brimstone Hill, beach or Basseterre plans to your ship day.</p>
        {disclaimer()}
        <div class="decision-chips">{year_links}</div>
        <div class="schedule-stats">
          <h2>{meta["callCount"]:,} scheduled calls</h2>
          <p>{meta["integrity"]["firstDate"]} to {meta["integrity"]["lastDate"]} · {meta["integrity"]["uniqueShips"]} ships · {meta["integrity"]["cruiseLines"]} cruise lines · {meta["integrity"]["populatedMonths"]} populated months</p>
          <p class="schedule-related"><a href="/{PORT_GUIDE}">Port &amp; terminal guide</a> · <a href="/{BEST_EXCURSIONS}">Excursion options</a> · <a href="/{ONE_DAY}">One-day planning</a></p>
        </div>
        <h2>Populated months</h2>
        <ul class="schedule-month-list">{month_links}</ul>
      </div>
    </section>
"""


def year_page(year: str, count: int, months: list[str], by_month: dict) -> str:
    links = "".join(
        f'<a class="decision-chip" href="{ym[5:]}/">{month_label(ym)} · {by_month[ym]}</a>'
        for ym in months
        if ym.startswith(year)
    )
    return f"""<!-- GENERATED FROM CARIBBEAN AUTHORITY - DO NOT MANUALLY EDIT -->
    <div class="page-hero page-hero--schedule">
      <div class="hero-bg" aria-hidden="true"></div>
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li><a href="/{HUB}/">Ship Schedule</a></li>
            <li aria-current="page">{year}</li>
          </ol>
        </nav>
        <h1>{esc(DEST)} cruise schedule {year}</h1>
        <p>{count} scheduled calls in {year}. Open a month to search by ship or date.</p>
      </div>
    </div>
    <section class="schedule-hub">
      <div class="container schedule-narrow">
        {disclaimer()}
        <div class="decision-chips">{links}</div>
        <p class="schedule-back"><a href="/{HUB}/">&larr; All years</a></p>
      </div>
    </section>
"""


def month_page(ym: str, calls: list[dict]) -> str:
    y, m = ym.split("-")
    label = month_label(ym)
    body = call_cards_html(sorted(calls, key=lambda c: (c["date"], c["ship"])))
    return f"""<!-- GENERATED FROM CARIBBEAN AUTHORITY - DO NOT MANUALLY EDIT -->
    <div class="page-hero page-hero--schedule">
      <div class="hero-bg" aria-hidden="true"></div>
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li><a href="/{HUB}/">Ship Schedule</a></li>
            <li><a href="/{HUB}/{y}/">{y}</a></li>
            <li aria-current="page">{label}</li>
          </ol>
        </nav>
        <h1>{label}: {esc(DEST)} cruise calls</h1>
        <p>{len(calls)} scheduled calls. Search by ship name or date below.</p>
      </div>
    </div>
    <section class="schedule-hub">
      <div class="container">
        {disclaimer()}
        <div class="schedule-month-body">{body}</div>
        <p class="schedule-back">
          <a href="/{HUB}/{y}/">&larr; {y} months</a>
          <a href="/{PORT_GUIDE}">Port guide</a>
          <a href="/{BEST_EXCURSIONS}">Excursions</a>
        </p>
      </div>
    </section>
"""


def sitemap_entries(months: list[str], years: list[str]) -> list[tuple[str, str, str]]:
    entries = [
        (f"{HUB}/", "0.8", "weekly"),
    ]
    for y in years:
        entries.append((f"{HUB}/{y}/", "0.7", "monthly"))
    for ym in months:
        y, m = ym.split("-")
        entries.append((f"{HUB}/{y}/{m}/", "0.6", "monthly"))
    return entries


def write_full_sitemap(schedule_entries: list[tuple[str, str, str]]) -> None:
    seen: set[str] = set()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, pri, freq in EDITORIAL_SITEMAP + schedule_entries:
        if path in seen:
            continue
        seen.add(path)
        loc = f"{DOMAIN}/" if not path else f"{DOMAIN}/{path}"
        lines.append(
            f"  <url><loc>{loc}</loc><changefreq>{freq}</changefreq><priority>{pri}</priority></url>"
        )
    lines.append("</urlset>")
    write(ROOT / "sitemap.xml", "\n".join(lines) + "\n")


def main() -> list[tuple[str, str, str]]:
    if not DATA.exists():
        raise SystemExit(f"Missing {DATA} - run node scripts/sync-schedules.mjs first")

    meta = json.loads(DATA.read_text(encoding="utf-8"))
    calls = meta["calls"]
    by_month: dict[str, list] = defaultdict(list)
    by_year: dict[str, int] = defaultdict(int)
    for c in calls:
        by_month[c["date"][:7]].append(c)
        by_year[c["date"][:4]] += 1

    months = sorted(by_month.keys())
    years = sorted(y for y, n in by_year.items() if n > 0 and y != "2028")

    hub_dir = ROOT / HUB
    if hub_dir.exists():
        for p in sorted(hub_dir.rglob("*"), reverse=True):
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                try:
                    p.rmdir()
                except OSError:
                    pass

    write(
        hub_dir / "index.html",
        page_shell(
            title=f"{esc(DEST)} Cruise Ship Schedule | Find Your Ship &amp; Date",
            description=f"{DEST} cruise ship schedule for cruise passengers: find your date and ship, then plan shore excursions around your Port Zante call.",
            canonical_path=f"{HUB}/",
            body_html=hub_page(meta, dict(by_year), months),
        ),
    )

    for y in years:
        write(
            hub_dir / y / "index.html",
            page_shell(
                title=f"{esc(DEST)} Cruise Schedule {y} | Ship Calls by Month",
                description=f"{DEST} cruise ship schedule for {y}: {by_year[y]} scheduled calls. Browse populated months and search by ship or date.",
                canonical_path=f"{HUB}/{y}/",
                body_html=year_page(y, by_year[y], months, meta["integrity"]["byMonth"]),
            ),
        )

    for ym, month_calls in by_month.items():
        y, m = ym.split("-")
        label = month_label(ym)
        write(
            hub_dir / y / m / "index.html",
            page_shell(
                title=f"{label} {esc(DEST)} Cruise Schedule | {len(month_calls)} Ship Calls",
                description=f"{DEST} cruise ship arrivals in {label}: {len(month_calls)} scheduled calls with ship names, cruise lines and planned arrival/departure times.",
                canonical_path=f"{HUB}/{y}/{m}/",
                body_html=month_page(ym, month_calls),
            ),
        )

    entries = sitemap_entries(months, years)
    frag = ROOT / "data" / "generated" / "schedule-sitemap.json"
    frag.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print(f"  wrote {frag.relative_to(ROOT)}")
    write_full_sitemap(entries)
    print(f"Schedule pages: hub + {len(years)} years + {len(months)} months")
    return entries


if __name__ == "__main__":
    main()
