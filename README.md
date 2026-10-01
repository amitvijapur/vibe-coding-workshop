# Vibe Coding Workshop

A beginner-friendly workshop by Amit Vijapur and Jason Cheng. Participants watch a venture idea become a working prototype, learn how to prompt and give feedback, then build a project of their own.

## Get the presentation

- [Present or download the HTML slides](out/vibe-coding-workshop.html)
- [Download the PowerPoint slides](out/vibe-coding-workshop.pptx)
- [Use the Durham housing demo prompt](docs/demo-prompt.md)

The deck has 19 slides. The HTML version is the animated presentation: it works offline, includes the images and logos, and advances one whole slide per click. The PowerPoint version is a static export with editable text and shapes. In the HTML deck, use **Space** or **→** to advance, **←** to go back, **O** for the slide overview, **N** for presenter notes and **F** for fullscreen. General Sans Regular and Medium should be installed locally for the intended typography; the font files are not included.

## Workshop flow

1. Meet the hosts and learn what vibe coding means.
2. Start a live Codex build while learning a five-part prompt: **Purpose, Design, Behaviour, Constraints, Verify**.
3. Review the result and practise the iteration loop: **Check, Describe, Change, Recheck, Save**. A useful feedback message says what happened, what was expected, what to keep and how to check the fix.
4. Take 5–10 minutes of questions, then give participants 30–45 minutes to build their own project.

The live demo is a Durham student housing prototype. It uses six fictional rentals and two fictional flatmate suggestions, runs on localhost, and is scoped for a 10–15 minute build. The [complete prompt](docs/demo-prompt.md) contains the brief and its limits. No live rental feeds or personal data are required.

## Build or change the slides

See [SETUP.md](SETUP.md) for dependencies and export commands. The content and slide layouts live in `build_slides.py`; `build_html.py` produces the HTML deck, and `web/` contains its player and styling. The generated files in `out/` are the two presentation downloads above. Edit the source files and regenerate both formats to keep them aligned. If you change the generated HTML directly, rebuilding it will replace those edits.

## Credits and reuse

Teaching ideas are adapted from [Chai Pin Zheng's workshop](https://github.com/Ducksss/vibe-coding-workshop), reviewed at commit `c896843a832bf0c6b4bdfa0714b763ce082a6c84`. The five-part brief comes from that workshop; our beginner feedback loop and live demo are adaptations. The visual direction references the opening slides of [Orange by Marmalade 2025](https://www.deck.gallery/orange-by-marmalade-2025/); the layouts here were created for this workshop.

Asset sources are recorded in the [tool-mark provenance](assets/tool-logos/PROVENANCE.md), [portrait provenance](assets/portraits/PROVENANCE.md) and [host-mark provenance](assets/brand/PROVENANCE.md). Portrait cutouts are edited derivatives of photos supplied for the workshop. Brand marks belong to their owners and do not imply endorsement. General Sans is not redistributed.

This repository does not include a blanket reuse licence. Public access to the files does not grant rights to third-party content, portraits, logos or fonts. Check the relevant rights before redistributing or adapting those materials.

## Presenters

- [Amit Vijapur](https://www.linkedin.com/in/amitvijapur/)
- [Jason Cheng](https://www.linkedin.com/in/jasoncty/)
