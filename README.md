# Café au Chromatic Homotopy — LaTeX authoring

Write normal LaTeX in `.tex` files. One source builds both a linked HTML website and a complete PDF. The topic files contain headings and labels only; the optional `examples/authoring.tex` demonstration is excluded by default.

## Install in your existing repository

1. Extract this ZIP locally. Copy **all contents of `cafe-latex/`**, including the hidden `.github/` folder, into the root of your existing repository. Do not upload the ZIP itself as the website.
2. Keep your old Markdown files as a backup if desired. The new build uses `main.tex`, so `_config.yml`, `_layouts/`, and the old Markdown pages no longer control the deployed site. This is a replacement publication pipeline, not a Jekyll plugin.
3. If `.github/workflows/` already contains a Pages deployment, disable/remove that older workflow to prevent competing deployments. Keep unrelated workflows.
4. Check your default branch name: `.github/workflows/pages.yml` assumes `main`. Change its `branches` entry if necessary.
5. On GitHub open **Settings → Pages → Build and deployment → Source → GitHub Actions**.
6. Commit and push. Open the repository's **Actions** tab, choose **Compile LaTeX and deploy Pages**, and check that both jobs pass. If you changed the Pages setting after the initial push, use **Run workflow**.
7. The deployment job supplies your site URL. Use that URL; there is no hardcoded repository name or `baseurl` to fix.

The first build installs TeX Live and can take several minutes. No repository access or live deployment has been performed by this download.

## Files you edit

- `main.tex`: title, author, chapter order, and bibliography.
- `preamble.tex`: packages, theorem environments, equation numbering.
- `macros.tex`: shared mathematical commands.
- `Preliminary/*.tex`, `ChromaticHomotopy/*.tex`, `FormalGroups/*.tex`, `AlgebraicGeometry/*.tex`: your notes.
- `references.bib`: your BibTeX entries.

The chapter index files use `\input{...}` to collect the topic files. The four main chapters become separate HTML pages, with sections linked from the table of contents. This starter does not assign Stacks Project style permanent tags; LaTeX labels provide cross-references within this book. Renaming/reordering chapters can change generated HTML filenames, so do not treat them as permanent public identifiers.

Some filenames were obscured in your screenshots. The clearly visible topic names have been retained, and `Morphisms.tex` and `FormalGroupLaws.tex` are explicit starter choices. Rename/add topics and update the corresponding chapter index as needed. No unseen Markdown content has been imported.

## Write a topic

Open `Preliminary/Spectra.tex`. It starts with:

```latex
\section{Spectra}\label{sec:preliminary-spectra}
% Write your notes here.
```

Write below that heading. Topic files are included fragments: do not give each one its own `\documentclass`, preamble, or `\begin{document}`.

```latex
\begin{definition}\label{def:my-definition}
Your definition goes here.
\end{definition}

\begin{theorem}[Optional name]\label{thm:my-theorem}
Your statement goes here.
\end{theorem}
\begin{proof}
Your proof goes here.
\end{proof}

See Theorem~\ref{thm:my-theorem}.

\begin{equation}\label{eq:my-equation}
  X \simeq Y.
\end{equation}
See equation~\eqref{eq:my-equation}.
```

Theorem, lemma, proposition, corollary, definition, example, and remark share a chapter-based counter. `proof` comes from `amsthm`. Give every label a unique name across all files. Standard `\ref`, `\eqref`, `\pageref`, `\cite`, `\href`, and `\url` are available. Page numbers are useful for the PDF; use `\ref` for navigation on the web.

## Bibliography

Add real BibTeX records to `references.bib`, then use `\cite{entry-key}` in a topic. Use `\nocite{entry-key}` or `\nocite{*}` in `main.tex` to include uncited entries. BibTeX and subsequent LaTeX passes resolve citations in both outputs. Before any citation is added, the build omits the empty bibliography so the blank starter still compiles.

To switch the style, replace `alpha` in `main.tex` with another installed BibTeX style such as `plain`. This setup uses BibTeX, not biblatex/Biber.

## Commands and compatibility

The macros from your old MathJax layout are now real LaTeX commands in `macros.tex`. Use `\Ocal`, `\Sphere`, `\Zp`, and `\Spec`; this avoids redefining the existing `\O` and `\S` commands and fixes underscore-containing command names.

The HTML is produced by TeX4ht through `make4ht`; math is displayed using MathJax, while LaTeX handles document structure, theorem numbering, cross-references, and citations. The PDF is genuinely typeset by pdfLaTeX. HTML reflows for the screen and will not have the identical page layout of the PDF. Arbitrary LaTeX packages, complex TikZ diagrams, custom classes, and custom math macros may require TeX4ht configuration; inspect both outputs after adding them. MathJax requires internet access in the reader's browser.

## Add a topic or chapter

1. Create a topic `.tex` file containing a `\section` and its text.
2. Add its `\input{Folder/Filename}` to the relevant chapter index.
3. For a new chapter, add a folder/index with `\chapter` and include it in `main.tex`. Also add the folder to the copy list in `scripts/build.sh` and the source list in `scripts/prepare_bibliography.py`.
4. Add local image assets inside one of the existing topic folders, and refer to them with repository-root-relative paths, e.g. `\includegraphics{Preliminary/figures/diagram.png}`.

## Build locally (optional)

With a full TeX Live installation (including make4ht), Python 3, and Bash:

```sh
bash scripts/build.sh
python3 -m http.server 8000 --directory _site
```

Open http://localhost:8000. On Debian/Ubuntu, the workflow lists the required packages. On Windows, use WSL or simply let GitHub Actions build for you. Output lives in `_site/`, with the PDF at `_site/cafe-au-chromatic-homotopy.pdf`. Do not edit generated HTML.

The build checks generated local links and anchors before uploading the site. Pull requests build without deploying; pushes to the configured branch deploy after a successful build. Branch protection and Pages environment policies can require GitHub-side approval.

## Sources

- https://github.com/michal-h21/make4ht
- https://www.kodymirus.cz/make4ht/make4ht-doc.html
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Validation of this starter

The PDF was compiled locally, including a separate temporary demonstration of theorem/equation references and BibTeX citations. Shell and Python syntax were checked. The HTML build and GitHub deployment could not be executed in the preparation environment because make4ht was not installed; check the first Actions run before relying on the published website.
