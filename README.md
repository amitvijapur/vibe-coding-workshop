# Vibe Coding Workshop

A beginner workshop by Amit Vijapur and Jason Cheng. Learn to describe a product, build with AI, inspect the result and improve it through useful feedback.

## Latest slides

- [Editable PowerPoint, v9](out/vibe-coding-workshop-draft-v9.pptx)
- [PDF preview, v9](out/vibe-coding-workshop-draft-v9.pdf)
- [Slide overview](out/v9-contact-sheet.jpg)

20 slides with presenter notes. Version 9 updates Amit's role to OpenAI Campus Ambassador. Older exports remain available. [Revision history](docs/deck-history.md).

## Workshop flow

Introduce the hosts and vibe coding. Launch the live Codex build and teach while it runs. Explain prompting and iteration, then inspect the demo and improve it. Take questions for 5–10 minutes before participants build a venture prototype for 30–45 minutes. Recap, connect and close.

The prompting framework is **Purpose, Design, Behaviour, Constraints, Verify**. The iteration loop is **Check, Describe, Change, Recheck, Save**. Useful feedback describes what happened, what was expected, what to keep and how to check.

## Demo

The chosen concept helps Durham students compare rental listings and find compatible flatmates. The first prototype uses clearly labelled fictional listings and profiles, not live website scraping, messaging or payments. This repository contains workshop material, not a completed rental application. The club-event chats remain small teaching examples.

The complete conversational prompt, framework mapping and live demonstration path are in [docs/demo-prompt.md](docs/demo-prompt.md).

## Build and edit

See [SETUP.md](SETUP.md) for installation, building and PDF export.

- `build_slides.py`: editable PowerPoint source and radial backgrounds.
- `render_review.py`: PDF previews and structural checks.
- `assets/`: photos, tool marks and provenance.
- `out/`: latest PowerPoint, PDF and contact sheet.

Install General Sans locally to preserve the editable layout; the PDF embeds its appearance. Fonts are not redistributed. Edit the builder, rebuild, export and visually inspect before pushing. Direct PowerPoint edits are not automatically imported into the builder.

## Sources and rights

Teaching concepts are adapted from [Chai Pin Zheng / Ducksss](https://github.com/Ducksss/vibe-coding-workshop), reviewed at commit `c896843a832bf0c6b4bdfa0714b763ce082a6c84`. The five-part brief comes from that workshop; the beginner feedback loop is our adaptation.

Visual direction references [Orange by Marmalade 2025](https://www.deck.gallery/orange-by-marmalade-2025/), with original editable layouts. The Karpathy quotation is sourced in presenter notes. See [v5 asset provenance](assets/v5/PROVENANCE.md) and [v6 asset provenance](assets/v6/PROVENANCE.md). Portrait cutouts are AI-edited derivatives of supplied photos. Brand marks belong to their owners and do not imply endorsement.

This is a private collaboration repository. No blanket open-source license is applied because third-party material, portraits, logos and fonts have separate rights. Confirm permission before public redistribution.

## Presenters

- [Amit Vijapur](https://www.linkedin.com/in/amitvijapur/)
- [Jason Cheng](https://www.linkedin.com/in/jasoncty/)

Before presenting, confirm tool access, timing, speaking roles and a saved live-demo fallback.
