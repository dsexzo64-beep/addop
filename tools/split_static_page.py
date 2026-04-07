"""
One-shot splitter: page_src.html -> index.html, assets/css/styles.css, assets/js/theme.js
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "page_src.html"
OUT_HTML = ROOT / "index.html"
OUT_CSS = ROOT / "assets" / "css" / "styles.css"
OUT_THEME = ROOT / "assets" / "js" / "theme.js"

# Prefix for paths that must load from the original host (GitHub static host has no _next)
ORIGIN = "https://www.playadopt.me"

STYLE_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.DOTALL | re.IGNORECASE)
# Inline script: has no src= attribute between <script and >
INLINE_SCRIPT_RE = re.compile(
    r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE
)


def absolutize_paths(text: str) -> str:
    """Point root-relative asset and page URLs at ORIGIN so the snapshot works off-site."""
    text = re.sub(
        r'(?<!https://www\.playadopt\.me)/_next/',
        ORIGIN + "/_next/",
        text,
    )
    replacements = [
        ('="/apple-', '="' + ORIGIN + "/apple-"),
        ('="/favicon', '="' + ORIGIN + "/favicon"),
        ('="/site.webmanifest', '="' + ORIGIN + "/site.webmanifest"),
        ('="/safari-pinned-tab', '="' + ORIGIN + "/safari-pinned-tab"),
    ]
    for a, b in replacements:
        text = text.replace(a, b)
    # Other same-site root paths (not protocol-relative //)
    text = re.sub(r'href="/(?!/)', f'href="{ORIGIN}/', text)
    return text


def main() -> None:
    raw = SRC.read_text(encoding="utf-8")

    styles: list[str] = []
    for m in STYLE_RE.finditer(raw):
        styles.append(m.group(1).strip())

    css = "\n\n/* ---- style block ---- */\n\n".join(styles)
    css = html.unescape(css)
    css = absolutize_paths(css)
    OUT_CSS.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSS.write_text(css, encoding="utf-8")

    inline_scripts: list[str] = []
    for m in INLINE_SCRIPT_RE.finditer(raw):
        block = m.group(1).strip()
        if not block:
            continue
        if "__NEXT_DATA__" in m.group(0):
            continue
        inline_scripts.append(html.unescape(block))

    theme_js = "\n\n".join(inline_scripts)
    OUT_THEME.parent.mkdir(parents=True, exist_ok=True)
    OUT_THEME.write_text(theme_js, encoding="utf-8")

    # Remove all style blocks
    html_no_style = STYLE_RE.sub("", raw)
    # Remove inline scripts we extracted (except __NEXT_DATA__)
    def _strip_inline(match: re.Match[str]) -> str:
        if "__NEXT_DATA__" in match.group(0):
            return match.group(0)
        return ""

    html_no_inline = INLINE_SCRIPT_RE.sub(_strip_inline, html_no_style)

    # Drop Next head bundles (hydration / not available on static host); keeps load clean
    html_no_inline = re.sub(
        r"\s*<script[^>]*src=[\"']/_next/[^\"']+[\"'][^>]*>\s*</script>\s*",
        "\n",
        html_no_inline,
        flags=re.IGNORECASE,
    )

    html_no_inline = absolutize_paths(html_no_inline)

    # Insert local CSS after charset viewport block (after first few meta)
    link_tag = f'    <link rel="stylesheet" href="assets/css/styles.css" />\n'
    if "assets/css/styles.css" not in html_no_inline:
        html_no_inline = html_no_inline.replace(
            "</title>\n", "</title>\n" + link_tag, 1
        )

    theme_tag = (
        '    <script src="assets/js/theme.js" defer></script>\n'
        if "assets/js/theme.js" not in html_no_inline
        else ""
    )
    # First line after <body>
    if theme_tag:
        html_no_inline = html_no_inline.replace("<body>\n", "<body>\n" + theme_tag, 1)

    OUT_HTML.write_text(html_no_inline, encoding="utf-8")
    print("Wrote", OUT_HTML.relative_to(ROOT))
    print("Wrote", OUT_CSS.relative_to(ROOT), "(%d bytes)" % OUT_CSS.stat().st_size)
    print("Wrote", OUT_THEME.relative_to(ROOT), "(%d bytes)" % OUT_THEME.stat().st_size)


if __name__ == "__main__":
    main()
