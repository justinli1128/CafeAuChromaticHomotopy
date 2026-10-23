#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
for tool in latexmk pdflatex bibtex make4ht python3; do
  command -v "$tool" >/dev/null || { echo "Missing required program: $tool" >&2; exit 1; }
done
# Fresh independent copies keep PDF and TeX4ht auxiliary files separate.
rm -rf build _site
mkdir -p build/pdf build/html _site
for target in build/pdf build/html; do
  cp main.tex preamble.tex macros.tex references.bib main.mk4 web.cfg "$target/"
  cp -R Preliminary ChromaticHomotopy FormalGroups AlgebraicGeometry examples "$target/"
done
# Suppress the bibliography until a topic contains its first citation.
# Only the private build copies are modified.
python3 scripts/prepare_bibliography.py build/pdf build/html
(
  cd build/pdf
  latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
)
(
  cd build/html
  make4ht -u -f html5 -c web.cfg -d ../../_site main.tex "mathjax,2"
)
cp build/pdf/main.pdf _site/cafe-au-chromatic-homotopy.pdf
cat > _site/index.html <<'HTML'
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Café au Chromatic Homotopy</title>
<meta http-equiv="refresh" content="0; url=main.html"></head>
<body><a href="main.html">Open Café au Chromatic Homotopy</a></body></html>
HTML
 touch _site/.nojekyll
python3 scripts/fix_toc_links.py
python3 scripts/check_site.py _site
