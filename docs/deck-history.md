# Vibe Coding Workshop

## Current HTML presentation, 1 October 2026

The actual presentation is now one current HTML deck at `out/vibe-coding-workshop.html`, edited in place. It preserves the 20-slide visual direction, adds browser reveals, navigation, overview and presenter notes, and includes Durham University, OpenAI and DragonFly logos on About Us. The demo prompt is scoped to a small localhost prototype designed for a 10 to 15 minute build. PowerPoint export is deferred until the HTML deck has been reviewed.

Version 9 updates Amit's host credential from AWS SBGL to OpenAI Campus Ambassador in the visible slide and presenter notes. All other workshop content remains unchanged from version 8.

Workshop review draft for Amit and Jason. The chosen venture demo helps Durham students compare rental listings and find compatible flatmates. The first prototype uses fictional listings and profiles; real integrations are outside this slide revision.

## Files

Latest: `out/vibe-coding-workshop-draft-v8.pptx` and matching PDF. Slide 5 now states the agreed Durham rental and flatmate demo concept. All other visible slides remain identical to v7.

Current: `out/vibe-coding-workshop-draft-v7.pptx` and matching PDF. Restores the original Check the result checklist at slide 13. Every other slide is unchanged from v6, verified by slide XML and rendered pixel comparison. Earlier versions remain available.

Latest: `out/vibe-coding-workshop-draft-v6.pptx` and matching PDF, with 20 editable slides. Includes transparent portrait cutouts, conversational prompting and feedback chat examples, a shorter iteration heading, a visual result-check example, venture-oriented activity ideas, both LinkedIn QR codes, and a thank-you slide. Preview: `out/v6-contact-sheet.jpg`. Version 5 is preserved. Image-editing prompts, asset paths and contact sources are recorded in `assets/v6/PROVENANCE.md`.

### Earlier revisions

Latest: `out/vibe-coding-workshop-draft-v5.pptx` and matching PDF. It applies all seven annotations on version 4, adding the DragonFly portraits, AWS SBGL credential, authentic tool marks and Lovable, a clearer beginner explanation and alternate Karpathy quote, requested headings, and an editable highlighted chat-style prompt example. Reviewed all changed slides and the full contact sheet, `out/v5-contact-sheet.jpg`. Asset sources are recorded in `assets/v5/PROVENANCE.md`.

Previous: `out/vibe-coding-workshop-draft-v4.pptx` and matching PDF. All topic titles are now large and direct; slide 4 explains Karpathy's original usage; tools include Claude and Claude Code; the iteration slide uses numbered rows; Q&A precedes project time. Preview: `out/v4-contact-sheet.jpg`. Earlier files below are retained revisions.

Current files: `out/vibe-coding-workshop-draft-v3.pptx` and matching PDF. Slide 6 now shows ChatGPT, Codex and Cursor with editable simplified interface illustrations; all other teaching content is unchanged from version 2. Preview: `out/v3-slide-06.png`.

Latest: `out/vibe-coding-workshop-draft-v2.pptx` and `out/vibe-coding-workshop-draft-v2.pdf`. Version 2 has 17 slides, adds beginner tool orientation, names the two frameworks, incorporates host details from the DragonFly deck, and includes participant project time and Q&A. Version 1 remains at the paths below and is also preserved in `out/v1/`.

- `out/vibe-coding-workshop-draft.pptx`: 12 editable slides with presenter notes.
- `out/vibe-coding-workshop-draft.pdf`: presentation preview with embedded fonts.
- `out/contact-sheet.jpg`: overview of the full deck.
- `out/slide-01.png` through `out/slide-12.png`: individual slide previews.

Typography uses General Sans, installed on Amit's Mac. Install the same family on other editing computers to preserve the PowerPoint layout. The PDF preserves the intended appearance without font installation. Text and diagrams are editable; the radial backgrounds are images.

Build source: `build_slides.py`. Review renderer: `render_review.py`. When exporting through LibreOffice, set `FONTCONFIG_FILE` to the absolute path of `assets/fonts.conf` so the installed fonts are found.

## Session structure

Introduce the hosts and vibe coding. Launch the Codex build early. Explain the prompting framework, iteration loop and useful feedback while it runs. Return to the result, compare it with the brief, and make one focused improvement.

Participants are complete beginners. The opening demo and instruction are followed by 5–10 minutes of Q&A, then 30–45 minutes for participants' own pet projects. Total event duration and official event name remain to be confirmed.

## Design direction

Reference: [Marmalade Brand Guidelines, slides 1 and 2](https://www.deck.gallery/orange-by-marmalade-2025/).

Use large black sans serif type, generous empty space, pale teaching backgrounds and softly blended radial colour fields. Orange, coral, pink and lilac are the primary reference, with blue, mint and yellow permitted as complementary variations. Gradients should support the hierarchy and preserve projected text legibility.

## Reused teaching material

[Chai Pin Zheng / Ducksss workshop](https://github.com/Ducksss/vibe-coding-workshop), reviewed at commit c896843a832bf0c6b4bdfa0714b763ce082a6c84.

- Source slide 4: definition, condensed and reworded.
- Source slide 9: describe, generate, inspect, refine, checkpoint loop.
- Source slides 10 and 12: specificity and five-part brief.
- Source slide 13: concrete follow-up feedback.
- Source slide 16 and facilitator guide: check observable results.

The new draft adapts these ideas into the agreed flow rather than reproducing the original lecture. Source credit uses the verified repository author. Preserve that credit when distributing. The public repository has no license file; confirm reuse terms with the creator before public redistribution.

Version 2 makes the feedback process a second explicit framework: Check, Describe, Change, Recheck, Save. Within Describe, participants state what happened, what they expected, what to keep and how to check. This is our beginner-oriented adaptation, not a verbatim framework attributed to Ducksss. The club-event prompt is an illustrative teaching example, not the live venture demo.

Recommended tool groups are ChatGPT / Claude, Codex / Claude Code, and Cursor / Lovable. Version 5 adds authentic brand visuals. Interface illustrations and the prompt conversation are teaching mockups, not screenshots. Tool roles are suggestions for beginners, not exclusive capability boundaries, and participants do not need every tool. References: https://help.openai.com/en/articles/12677804-what-is-chatgpt-faq, https://openai.com/codex/, https://cursor.com/, https://lovable.dev/, https://support.anthropic.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan. Participant tool access must be arranged before the session. No subscription or free-access claim is implied.

The origin slide references Andrej Karpathy's February 2025 post: https://x.com/karpathy/status/1886192184808149383. Direct retrieval was blocked; version 5's alternate short quotation is verified against the post transcription at https://threadreaderapp.com/thread/1886192184808149383.html and https://www.figma.com/blog/double-click-vibe-coding/. The short quote is distinguished from our explanatory paraphrase. The beginner claim concerns making a first prototype, not safely launching a production product without review.

## Decisions for the host review

- Host introductions are sourced from the DragonFly deck, including Durham backgrounds and DragonFly roles.
- Choose a venture idea with one clear action that can be demonstrated.
- Write the final demo prompt using the five-part framework.
- Confirm event name, overall duration and participant tool access.
- Rehearse the build with the actual account and tool access, and retain a saved fallback.

Use fictional demo data. Treat Codex's completion summary as something to verify by operating the result.
