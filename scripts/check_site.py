"""Check generated local pages, fragments, assets, and the PDF before deployment."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys
root = Path(sys.argv[1]).resolve()
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = set(); self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ('id', 'name'):
            if a.get(key): self.ids.add(a[key])
        for key in ('href', 'src'):
            if a.get(key): self.links.append(a[key])
pages = {}
for path in root.rglob('*.html'):
    page = Page(); page.feed(path.read_text()); pages[path] = page
errors = []
for path, page in pages.items():
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc or link.startswith('data:'): continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if not target.exists(): errors.append(f'{path.name}: missing {link}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{path.name}: missing anchor {link}')
for required in ('index.html', 'main.html', 'cafe-au-chromatic-homotopy.pdf'):
    if not (root / required).is_file(): errors.append(f'Missing {required}')
if errors: raise SystemExit('\n'.join(errors))
print(f'Validated {len(pages)} HTML pages and their local links.')
