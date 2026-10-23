"""Disable empty bibliographies in build copies, leaving source files unchanged."""
from pathlib import Path
import re
import sys
for name in sys.argv[1:]:
    root = Path(name)
    sources = [root / 'main.tex']
    for folder in ('Preliminary', 'ChromaticHomotopy', 'FormalGroups', 'AlgebraicGeometry'):
        sources.extend((root / folder).glob('*.tex'))
    text = '\n'.join(re.sub(r'(?<!\\)%.*', '', p.read_text()) for p in sources)
    if not re.search(r'\\(?:cite\w*|nocite)\s*(?:\[[^\]]*\]\s*)*\{', text):
        main = root / 'main.tex'
        main.write_text(main.read_text().replace(r'\bibliographystyle{alpha}', '').replace(r'\bibliography{references}', ''))
        mk4 = root / 'main.mk4'
        mk4.write_text(mk4.read_text().replace('Make:bibtex()\n', ''))
