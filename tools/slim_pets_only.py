"""Strip index.html to pets list + pet card links only (no site chrome, no __NEXT_DATA__)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "index.html"
OUT = ROOT / "index.html"

HEAD = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <meta name="description" content="Pets collection" />
    <title>Pets</title>
    <link rel="preconnect" href="https://use.typekit.net" crossorigin="" />
    <link rel="stylesheet" href="https://www.playadopt.me/_next/static/css/029e8b0ddf0cd0b1.css" />
    <link rel="stylesheet" href="assets/css/styles.css" />
    <style id="pets-event-fallback">
      .pets-event-banner,.pets-event-title,.pets-event-timer{display:block!important;visibility:visible!important;opacity:1!important}
    </style>
  </head>
  <body class="pets-page-only">
    <script src="assets/js/theme.js" defer></script>
"""

FOOT = """    <script src="assets/js/event-countdown.js"></script>
  </body>
</html>
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    m = re.search(r"(?s)(<main id=\"main\"[^>]*>)(.*?)(</main>)", text)
    if not m:
        raise SystemExit("Could not find <main id=\"main\">")
    main_open, main_body, main_close = m.group(1), m.group(2), m.group(3)

    main_body = re.sub(
        r"\s*<a aria-label=\"Back\" href=\"\./\" class=\"css-1szvqd4 ecs7b861\">.*?</a>\s*",
        "\n            ",
        main_body,
        count=1,
        flags=re.DOTALL,
    )

    out = HEAD + "\n" + main_open + main_body + main_close + "\n" + FOOT
    OUT.write_text(out, encoding="utf-8")
    print("Wrote slim page, chars:", len(out))


if __name__ == "__main__":
    main()
