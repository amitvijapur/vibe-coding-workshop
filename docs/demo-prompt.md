# Durham student renting demo prompt

## Demo concept

A localhost-only prototype that helps Durham students shortlist a fictional rental and find compatible fictional flatmates.

## Prompt to use

Hey, I want to make a small app that helps Durham students find somewhere to rent and people to live with. Looking across lots of rental websites is frustrating, so I want to show how listings from different places could sit in one simple product.

Please build a polished single-page prototype using plain HTML, CSS and JavaScript. Run it only on localhost. Make it feel welcoming and trustworthy, and make sure it works on a phone-sized screen at 390 × 844 pixels.

Use six clearly labelled fictional Durham properties. Let me choose a maximum weekly rent and an area, then show the matching properties. Each card should include a photo placeholder, weekly rent, bedrooms, area, whether bills are included and a fictional source name. Let me shortlist one property.

After I shortlist a property, show a **Find your flatmate** step. Let me choose two living preferences, then recommend two fictional flatmate profiles and explain the preferences we share.

I've only got 10 to 15 minutes for this demo, so keep this first version deliberately small. Use hard-coded sample data. Do not add accounts, a database, live website scraping, external APIs, maps, real messaging, payments or deployment. Do not install extra packages unless the existing project truly needs them.

Please check that:

- the app opens on localhost;
- changing the rent and area filters changes the visible properties;
- I can shortlist one property;
- the flatmate suggestions reflect the two preferences I choose; and
- the full journey is usable at a 390 × 844 phone-sized viewport.

When it works, tell me the local URL and give me a short summary of what you checked.

## Build boundary

This is designed for a 10–15 minute live build. The complete journey is:

1. Set a budget and area.
2. Choose one fictional property.
3. Choose two living preferences.
4. See two fictional flatmate suggestions with a short explanation.

Anything beyond that journey is out of scope for the workshop demo.

## How it fits the framework

| Framework part | What it covers |
| --- | --- |
| Purpose | Help Durham students shortlist a rental and identify compatible flatmates. |
| Design | Welcoming, trustworthy and mobile-friendly. |
| Behaviour | Filter listings, shortlist one property and generate two explained flatmate suggestions. |
| Constraints | One static page on localhost, hard-coded fictional data and no integrations or user accounts. |
| Verify | Open locally, test both filters, shortlist one property, test matching and repeat the journey at 390 × 844. |

## Live demonstration path

Pick a maximum weekly rent and area, shortlist one matching property, choose two living preferences and view the two suggested flatmates.

Use fictional data throughout. Inspect the result yourself, give one concrete follow-up prompt and keep a clearly labelled prepared fallback in case the live generation is unfinished.
