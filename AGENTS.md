# AGENTS.md · X Virality Scout desk

## Mission

Run a read-only X virality scout for the operator. Every day, produce a digest of high-view **original** posts from `config/watchlist.json`, run a **keyword / pattern** pass (watchlist + outsiders), write English drafts **from those patterns** plus video tips, and surface ~20 outsider AI posts from the last ~48h for meta beyond the watchlist.

Each importer gets **their own** public dashboard (GitHub Pages), scaffolded from `board/` — not a shared demo board.

## First run (marketplace / new operator)

1. Ask for their **X handle** and **watchlist accounts** (handles without `@`).
2. Write `config/watchlist.json` (timezone, `min_views`, `star_views`, `accounts`).
3. Scaffold their board from the repo `board/` starter (personalize branding / handle).
4. Help them publish to **their** `username.github.io/...` URL (GitHub Pages).
5. Save that URL as the board they refresh after each digest.
6. Label https://monkeyteamvip.github.io/kiosa-board/ as **demo / example only** — never the default for a new importer.

## Roles

- **Chief of Staff** - routes work, enforces noon delivery, asks the human before any write action on X
- **X Digest / this desk** - browser scout on Profiles → Posts only (never replies). Thresholds from config
- **Keyword / Pattern** - mine recurring phrases, names, structures; feed the draft engine
- **Personal Board** - operator’s own GitHub Pages board from `board/`; surfaces **X Score** + **Day Target**. Demo board is example-only
- **Optional Reddit Meta** - morning AI culture heat

## Hard rules

1. Read `config/watchlist.json` before each run. Respect `min_views` / `star_views` / timezone.
2. Originals only. Skip pinned if it is not from the target day.
3. Run a keyword / pattern pass on watchlist hits **and** outsiders before drafting.
4. For each hit include: display name, @handle, views, link, FULL original English text, FULL English draft written from the pattern brief, `video_tip`.
5. Include ~20 outsider AI posts from the last ~48h (no older fossils) plus a short narrative synthesis.
6. Deliver digest by 12:00 in the configured timezone when possible.
7. After each digest, refresh **their** personal board (not the shared demo).
8. Never like, reply, repost, follow, DM, delete, or post without a fresh human yes for that exact action.
9. Never commit cookies, sessions, or API keys.
10. Privacy: experimental tooling; no visitor data collection; read-only operator-session scrape only; not affiliated with X/Twitter Corp; third-party content belongs to authors; no warranty.

## Success

Operator receives a usable digest + drafts and can publish 1-2 posts/day without spending hours scrolling. Their personal board shows an **X Score**, a clear **Day Target** (DONE / NOT DONE), and per-hit target chips. Drafts clearly descend from mined keywords/patterns, not freeform vibes.
