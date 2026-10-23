# SB Web Factory — AI Agent Team for Client Websites

**Role: the free AI team that builds every SB AI Studio client website.**
No Base44 credits, no sub-agents. Runs entirely on free tools:
GitHub (public repo, unlimited Actions minutes) + deterministic template engine.
Solas is the team admin/architect. Workers are pipeline stages.

## The Team

1. *Solas (Admin & Architect)* — closes the deal, interviews the client, writes the spec JSON, reviews QA, delivers the live demo link, handles revisions. Base44 credits used only for normal chat, never sub-agents.
2. *The Spec* — `specs/<slug>.json`, the complete blueprint: business info, theme colors, sections, menu/services, booking type, SEO.
3. *The Builder* — `generate.py` renders the full premium website from the spec in seconds.
4. *QA* — validates required fields, slug format, no unrendered placeholders, sane output size; fails on any issue.
5. *Deployer* — GitHub Pages publishes to https://selimsb645-max.github.io/sb-web-factory/sites/<slug>/
6. *Copy AI (phase 2, optional)* — free Gemini API tier can draft business copy into the spec automatically.

## How an order flows

1. Client says yes (Solas closes, per standing instruction).
2. Solas writes `specs/<business-slug>.json` from the client interview or their old site.
3. Solas runs `python3 generate.py` and pushes. Pages deploys within ~2 minutes.
4. Solas reviews the preview link and sends it to the client as their free demo.
5. Revisions = edit the spec, regenerate, push again.
6. Client's own domain is connected later; the same files serve it.

## Rules

- NEVER put client personal data beyond public business contact info in specs (repo is public).
- NEVER commit tokens/cookies/credentials here.
- One spec per client; slug = preview URL path.
- Specs are the single source of truth — edit specs, never rendered HTML.

## Local usage

```bash
python3 generate.py          # renders specs/*.json -> sites/*/index.html
```
