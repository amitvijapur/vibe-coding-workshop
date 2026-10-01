# Build and present the workshop deck

Run these commands from the repository root. Use Python 3.11 or later; the reviewed build used Python 3.12.14. No API key is needed.

## Install

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1` in PowerShell.

Install General Sans Regular and Medium locally from its official distributor and follow its licence. The repository does not bundle font files. Without them, browsers and PowerPoint may substitute another font and alter line wrapping.

## Generate the presentations

```sh
python build_html.py
python build_slides.py
```

These commands update `out/vibe-coding-workshop.html` and `out/vibe-coding-workshop.pptx`. Both use the shared slide content in `build_slides.py`. Run both after changing slide copy or layouts so the downloads stay aligned. Changes made directly to a generated file will be overwritten on the next build.

Open the HTML file in a browser to present it. It contains its images, styles and navigation, so a web server and internet connection are unnecessary. Space or the right arrow advances one slide; the left arrow goes back. Press O for the overview, N for notes and F for fullscreen. The HTML deck has one automatic fade per slide, with all of that slide's content visible at once.

The PowerPoint is a static export with editable text and shapes. Check the layout on the computer used for presenting, especially if fonts differ.

## Optional PDF review

Install LibreOffice separately and make `soffice` available on your command path. On macOS, you may need `/Applications/LibreOffice.app/Contents/MacOS/soffice` instead.

```sh
soffice --headless --convert-to pdf --outdir out out/vibe-coding-workshop.pptx
python render_review.py vibe-coding-workshop
```

The PDF and contact sheet are local review outputs, not additional published presentation versions. `render_review.py` checks slide and page counts, presenter notes and slide bounds. Visually inspect the result before distributing a new build. If LibreOffice cannot see General Sans, fix the font installation or local fontconfig setup. The development `assets/fonts.conf` uses machine-specific paths and is intentionally ignored by Git.

## Source layout

- `build_slides.py` defines the slide content and generates the PowerPoint.
- `build_html.py` turns that content into the self-contained HTML presentation.
- `web/` contains the browser shell, styles and navigation.
- `docs/demo-prompt.md` contains the live-build prompt and teaching notes.
- `assets/tool-logos/`, `assets/portraits/` and `assets/brand/` contain the source marks, photos, cutouts and provenance needed for the build.
- `out/` publishes only the current HTML and PowerPoint files. Other generated previews are ignored.

Keep the provenance files with the assets. Brand marks and portraits have separate rights; the repository does not grant a new licence to them or to General Sans.

Optional browser verification uses Node.js, Playwright, Sharp and an installed Chrome browser. Run `node check_html.cjs` after making changes to the HTML player. It tests navigation and captures a local contact sheet.
