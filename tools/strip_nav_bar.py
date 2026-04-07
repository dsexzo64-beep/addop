from pathlib import Path

p = Path(__file__).resolve().parents[1] / "index.html"
t = p.read_text(encoding="utf-8")

# 1) Desktop: News → Merch (keep Discover)
start = t.find(
    '<div class="css-c0nxyw e117kliq0">\n                \n                <a aria-current="false" href="https://www.playadopt.me/news"'
)
end = t.find("\n            <div class=\"css-1lt835l e1nzkhij16\">", start)
if start == -1 or end == -1:
    raise SystemExit("desktop nav block not found")
t = t[:start] + t[end:]

# 2) Desktop: Play + theme row
a_start = t.find('<div class="css-1a4gfaj e1nzkhij10">')
a_end = t.find("\n            \n            <div class=\"css-1dppe18\">", a_start)
if a_start == -1 or a_end == -1:
    raise SystemExit("play/theme block not found")
t = t[:a_start] + t[a_end:]

# 3) Mobile: first bm-item (play + theme)
b_start = t.find('<div class="bm-item css-xmaie8 e1nzkhij8"')
if b_start == -1:
    raise SystemExit("bm-item not found")
b_end = t.find(
    "\n                      <div class=\"css-c0nxyw e117kliq0\">\n                        <a aria-current=\"page\" href=\"https://www.playadopt.me/discover\"",
    b_start,
)
if b_end == -1:
    raise SystemExit("after bm-item not found")
t = t[:b_start] + t[b_end:]

# 4) Mobile: News → Merch (keep Discover)
m_start = t.find(
    '<div class="css-c0nxyw e117kliq0">\n                        <a aria-current="false" href="https://www.playadopt.me/news"',
)
m_end = t.find("\n                    </nav>", m_start)
if m_start == -1 or m_end == -1:
    raise SystemExit("mobile news-merch not found")
t = t[:m_start] + t[m_end:]

p.write_text(t, encoding="utf-8")
print("OK:", p)
