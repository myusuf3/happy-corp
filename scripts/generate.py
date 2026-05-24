#!/usr/bin/env python3
"""Build joy-of-the-day static pages from data/joys.json.

Run this when content changes. Output is checked into git.
"""

import json
import shutil
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "joys.json"
DAYS_DIR = ROOT / "d"
ROOT_INDEX = ROOT / "index.html"

WEEKDAYS = [
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday",
]
MONTHS = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
]


def humanize(d: date) -> str:
    return f"{WEEKDAYS[d.weekday()]}, {MONTHS[d.month - 1]} {d.day}, {d.year}"


# Umami analytics — privacy-respecting, no cookies, no PII, self-hosted.
# See privacy.html for what is and isn't collected.
ANALYTICS_STUB = '    <script async src="https://umami.booq.cc/script.js" data-website-id="62378df5-6c68-4ab8-a7f0-e1b20f31f91c"></script>'


DAY_TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{copy} — happy corp</title>
    <meta name="description" content="happy corp — a tiny moment of joy for {human_date}." />
    <meta name="theme-color" content="#fff7d6" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="stylesheet" href="../../styles.css" />
  </head>
  <body>
    <main class="joy">
      <p class="joy-visual" aria-hidden="true">{emoji}</p>
      <p class="joy-copy">{copy}</p>
      <p class="joy-date">{human_date}</p>
      <p class="about">one tiny, handcrafted moment of joy, every day. that’s the whole thing.</p>
    </main>
    <footer>
      <a href="../../">today’s joy</a>
      <span aria-hidden="true"> · </span>
      <a href="../../privacy.html">privacy</a>
    </footer>
{analytics}
  </body>
</html>
"""


ROOT_TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>happy corp — a tiny moment of joy</title>
    <meta name="description" content="happy corp — one tiny, handcrafted moment of joy every day." />
    <meta name="theme-color" content="#fff7d6" />
    <link rel="icon" type="image/svg+xml" href="favicon.svg" />
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <main class="joy" aria-live="polite">
      <p class="joy-visual" aria-hidden="true" id="joy-visual">{fallback_emoji}</p>
      <p class="joy-copy" id="joy-copy">{fallback_copy}</p>
      <p class="joy-date" id="joy-date">a tiny moment of joy</p>
      <p class="about">one tiny, handcrafted moment of joy, every day. that’s the whole thing.</p>
    </main>
    <footer>
      <a href="privacy.html">privacy</a>
    </footer>
    <script id="joys-data" type="application/json">{joys_json}</script>
    <script>
      (function () {{
        try {{
          var node = document.getElementById("joys-data");
          if (!node) return;
          var data = JSON.parse(node.textContent);
          if (!Array.isArray(data) || data.length === 0) return;
          var weekdays = {weekdays_js};
          var months = {months_js};
          function pad(n) {{ return n < 10 ? "0" + n : "" + n; }}
          function humanize(d) {{
            return weekdays[(d.getDay() + 6) % 7] + ", " + months[d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear();
          }}
          var now = new Date();
          var todayIso = now.getFullYear() + "-" + pad(now.getMonth() + 1) + "-" + pad(now.getDate());
          var entry = null;
          for (var i = 0; i < data.length; i++) {{
            if (data[i].date === todayIso) {{ entry = data[i]; break; }}
          }}
          if (!entry) {{
            var first = new Date(data[0].date + "T00:00:00");
            var todayLocal = new Date(now.getFullYear(), now.getMonth(), now.getDate());
            var diff = Math.floor((todayLocal - first) / 86400000);
            var idx = ((diff % data.length) + data.length) % data.length;
            entry = data[idx];
          }}
          document.getElementById("joy-visual").textContent = entry.emoji;
          document.getElementById("joy-copy").textContent = entry.copy;
          document.getElementById("joy-date").textContent = humanize(now);
          document.title = entry.copy + " — happy corp";
        }} catch (err) {{ /* keep static fallback */ }}
      }})();
    </script>
{analytics}
  </body>
</html>
"""


def main() -> None:
    joys = json.loads(DATA_FILE.read_text())
    joys.sort(key=lambda j: j["date"])

    if DAYS_DIR.exists():
        shutil.rmtree(DAYS_DIR)
    DAYS_DIR.mkdir(parents=True)

    for entry in joys:
        d = datetime.strptime(entry["date"], "%Y-%m-%d").date()
        day_dir = DAYS_DIR / entry["date"]
        day_dir.mkdir(parents=True, exist_ok=True)
        html = DAY_TEMPLATE.format(
            copy=entry["copy"],
            emoji=entry["emoji"],
            human_date=humanize(d),
            analytics=ANALYTICS_STUB,
        )
        (day_dir / "index.html").write_text(html, encoding="utf-8")

    fallback = joys[0]
    root_html = ROOT_TEMPLATE.format(
        joys_json=json.dumps(joys, ensure_ascii=False),
        fallback_emoji=fallback["emoji"],
        fallback_copy=fallback["copy"],
        weekdays_js=json.dumps(WEEKDAYS),
        months_js=json.dumps(MONTHS),
        analytics=ANALYTICS_STUB,
    )
    ROOT_INDEX.write_text(root_html, encoding="utf-8")

    print(f"Wrote {len(joys)} day pages and root index.html.")


if __name__ == "__main__":
    main()
