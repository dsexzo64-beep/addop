from pathlib import Path

p = Path(__file__).resolve().parents[1] / "index.html"
t = p.read_text(encoding="utf-8")
old = '<a href="https://www.playadopt.me/discover/pets/'
new = '<a target="_blank" rel="noopener noreferrer" href="https://www.playadopt.me/discover/pets/'
c = t.count(old)
t = t.replace(old, new)
p.write_text(t, encoding="utf-8")
print("replaced", c)
