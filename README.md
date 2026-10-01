# Vibe Coding Workshop

A beginner workshop by Amit Vijapur and Jason Cheng. Learn to describe a product, build with AI, inspect the result and improve it through useful feedback.

## Current presentation

- [Open the HTML presentation](out/vibe-coding-workshop.html)
- [Review the demo prompt](docs/demo-prompt.md)

19 slides with presenter notes and one automatic fade per slide. All content appears together, and each click advances to the next slide. This is the single working deck, updated in place. Open the HTML file in a browser. It includes the photos and logos and works offline. PowerPoint export will be refreshed after the HTML presentation is reviewed. Amit's role is OpenAI Campus Ambassador, and the About Us slide includes equally sized affiliation marks under each host's biography.

Use Space or the right arrow to advance one slide. Left arrow goes back. O opens the slide list, N opens presenter notes and F enters fullscreen. The presentation honours reduced-motion settings. General Sans should be installed locally for the intended typography.

## Workshop flow

Introduce the hosts and vibe coding. Launch the live Codex build and teach while it runs. Explain prompting and iteration, then inspect the demo and improve it. Take questions for 5–10 minutes before participants build a venture prototype for 30–45 minutes. Recap, connect and close.

The prompting framework is **Purpose, Design, Behaviour, Constraints, Verify**. The iteration loop is **Check, Describe, Change, Recheck, Save**. Useful feedback describes what happened, what was expected, what to keep and how to check.

## Demo

The demo is scoped for a 10 to 15 minute build of a single page on localhost. Filter six fictional rentals, shortlist one property, choose two living preferences and see two explained flatmate suggestions. The prompt excludes accounts, databases, scraping, external APIs, maps, messaging, payments and deployment. The club-event chats remain small teaching examples.

The complete conversational prompt, framework mapping and live demonstration path are in [docs/demo-prompt.md](docs/demo-prompt.md).

## Build and edit

See [SETUP.md](SETUP.md) for installation, building and PDF export.

- `build_slides.py`: shared editable content and radial backgrounds.
- `build_html.py`: the current HTML presentation builder.
- `web/`: browser presentation controls, styling and HTML shell.
- `render_review.py`: PDF previews and structural checks.
- `assets/`: photos, tool marks and provenance.
- `out/`: current HTML presentation and historical PowerPoint/PDF exports.

Install General Sans locally to preserve the intended layout. Fonts are not redistributed. Edit the shared content or web player, rebuild with `python build_html.py`, and review the current HTML file. Direct PowerPoint edits are not automatically imported into the builder.

## Sources and rights

Teaching concepts are adapted from [Chai Pin Zheng / Ducksss](https://github.com/Ducksss/vibe-coding-workshop), reviewed at commit `c896843a832bf0c6b4bdfa0714b763ce082a6c84`. The five-part brief comes from that workshop; the beginner feedback loop is our adaptation.

Visual direction references [Orange by Marmalade 2025](https://www.deck.gallery/orange-by-marmalade-2025/), with original editable layouts. The Karpathy quotation is sourced in presenter notes. See [v5 asset provenance](assets/v5/PROVENANCE.md), [v6 asset provenance](assets/v6/PROVENANCE.md) and [host logo provenance](assets/v10/PROVENANCE.md). Portrait cutouts are AI-edited derivatives of supplied photos. Brand marks belong to their owners and do not imply endorsement.

This is a private collaboration repository. No blanket open-source license is applied because third-party material, portraits, logos and fonts have separate rights. Confirm permission before public redistribution.

## Presenters

- [Amit Vijapur](https://www.linkedin.com/in/amitvijapur/)
- [Jason Cheng](https://www.linkedin.com/in/jasoncty/)

Before presenting, confirm tool access, timing, speaking roles and a saved live-demo fallback.
