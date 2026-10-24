"""Repair TeX4ht navigation fragments without hiding broken content references."""
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("id", "name") and value:
                self.ids.add(value)


pages = {}
for path in root.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    anchors = Anchors()
    anchors.feed(text)
    pages[path] = (text, anchors.ids)

href = re.compile(r'''\bhref\s*=\s*(["'])(.*?)\1''', re.IGNORECASE)
# TeX4ht sometimes puts an output filename in the fragment of an Up link.
output_name = re.compile(r"main(?:ch|li|se|su|ss)\d+\.html")
repaired = 0
for path, (text, _) in pages.items():
    def repair(match):
        global repaired
        url = urlsplit(unescape(match.group(2)))
        if url.scheme or url.netloc or not url.fragment:
            return match.group(0)
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target not in pages:
            return match.group(0)
        fragment = unquote(url.fragment)
        if fragment in pages[target][1]:
            return match.group(0)
        generated_navigation = (
            output_name.fullmatch(fragment)
            and (target.parent / fragment).resolve() in pages
        )
        if not generated_navigation and not (
            fragment == "_" and target == root / "main.html"
        ):
            return match.group(0)
        # Keep the parent page destination, dropping only its bogus fragment.
        value = match.group(2).rsplit("#", 1)[0]
        if not value:
            return match.group(0)
        repaired += 1
        return f'href={match.group(1)}{value}{match.group(1)}'

    updated = href.sub(repair, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")

print(f"Repaired {repaired} TeX4ht navigation links.")
