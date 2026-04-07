"""
Download pet thumbnails from cdn.playadopt.me into assets/pets/items/
and fix index.html img tags to use local files.
"""
from __future__ import annotations

import re
import ssl
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
OUT_DIR = ROOT / "assets" / "pets" / "items"

IMG_RE = re.compile(
    r'<img alt="([^"]*)" src="data:image/gif;base64,R0lGODlhAQAB[^"]*" decoding="async" data-nimg="intrinsic" class="css-0 e12aqbjs2" style="[^"]*"\s*/>'
)
SEED_RE = re.compile(r'seed="(https://cdn\.playadopt\.me/items/[^"]+)"')


def download_one(url: str, dest: Path, ctx: ssl.SSLContext) -> bool:
    if dest.exists() and dest.stat().st_size > 100:
        return True
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (compatible; PetMirror/1.0)"}
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            dest.write_bytes(r.read())
        return True
    except Exception as e:
        print("FAIL", url, e)
        return False


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    urls = sorted(set(SEED_RE.findall(html)))
    print("unique images:", len(urls))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context()

    ok = 0
    for i, url in enumerate(urls):
        name = url.rsplit("/", 1)[-1]
        dest = OUT_DIR / name
        if download_one(url, dest, ctx):
            ok += 1
        if (i + 1) % 100 == 0:
            print(i + 1, "/", len(urls))
        time.sleep(0.02)

    print("downloaded ok:", ok, "/", len(urls))

    html = html.replace(
        "https://cdn.playadopt.me/items/", "assets/pets/items/"
    )

    SEED_LOCAL = re.compile(r'seed="(assets/pets/items/[^"]+)"')
    pos = 0
    repl_count = 0
    while True:
        m = SEED_LOCAL.search(html, pos)
        if not m:
            break
        local = m.group(1)
        start = m.end()
        m2 = IMG_RE.search(html, start, start + 5000)
        if not m2:
            pos = start
            continue
        alt = m2.group(1)
        new_img = (
            f'<img alt="{alt}" src="{local}" loading="lazy" decoding="async" '
            'class="css-0 e12aqbjs2" '
            'style="position:absolute;top:0;left:0;bottom:0;right:0;box-sizing:border-box;'
            "padding:0;border:none;margin:auto;display:block;width:0;height:0;"
            'min-width:100%;max-width:100%;min-height:100%;max-height:100%;object-fit:contain" />'
        )
        html = html[: m2.start()] + new_img + html[m2.end() :]
        repl_count += 1
        pos = m2.start() + len(new_img)

    print("img tags replaced:", repl_count)
    INDEX.write_text(html, encoding="utf-8")
    print("Wrote", INDEX)


if __name__ == "__main__":
    main()
