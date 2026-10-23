from pathlib import Path
import re

root = Path("_site")
pattern = re.compile(
    r"""href=(["'])main\.html#(main(?:ch|li)\d+\.html)\1"""
)

for page in root.glob("*.html"):
    def repair(match):
        if (root / match.group(2)).is_file():
            return f'href={match.group(1)}main.html{match.group(1)}'
        return match.group(0)

    page.write_text(pattern.sub(repair, page.read_text()))
