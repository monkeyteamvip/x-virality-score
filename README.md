# X Virality Score

A practical **X/Twitter virality desk** you run with Grok Bot agents.

It watches a list of accounts you choose, finds original posts that already cleared a view threshold, runs a **keyword / pattern** pass, and drops you:

- the full original text
- an English draft written **from mined keywords and patterns** (different angle)
- a short `video_tip` for what to shoot
- ~20 **outsider** AI posts from the last ~48h (meta beyond your watchlist)
- a daily digest you can open before noon
- a public **Grok Bot X Virality Score** board with X Score + Day Target

This is not an auto-poster and not an engagement farm. You stay the publisher.

## What you get

1. **Watchlist virality check** - swap in your own handles in `config/watchlist.json`
2. **Keyword / pattern pass** - recurring phrases, names, structures from watchlist + outsiders
3. **Drafts from those patterns** - EN draft + `video_tip`, not vibes
4. **Outsiders meta** - ~20 AI posts / last ~48h beyond your list
5. **Daily digest + Grok Bot X Virality Score board** - X Score, Day Target DONE/NOT DONE, per-hit chips
6. **Article case study** - how one operator staffed a mini agency with agents (`ARTICLE.md`)

## Quick start

1. Copy the example watchlist and edit handles:

```bash
cp config/watchlist.example.json config/watchlist.json
# put your accounts in "accounts"
```

2. Point your Grok Bot / Chief of Staff at this repo (or paste `AGENTS.md` into the agent that owns digests).

3. Keep a logged-in X session on the box browser for **read-only** scrolling. Do not commit cookies, tokens, or API keys.

4. Run the daily loop described in `docs/daily-loop.md`.

## Config

`config/watchlist.json`

- `timezone` - when "yesterday" is calculated (default `Europe/Moscow`)
- `min_views` - floor for a hit (default `5000`)
- `star_views` - highlight threshold (default `10000`)
- `accounts` - list of handles **without** `@`

Anyone can fork this and track a totally different niche (AI tools, memecoins, design, local news). The scout logic stays the same.

## Privacy / experimental

- Experimental personal tooling. No warranty.
- No personal data collection from board visitors. No tracking cookies (local UI state only if any).
- X is scraped read-only via the **operator** session on the box, never via visitor accounts.
- Not affiliated with X Corp / Twitter, Inc.
- Third-party posts remain owned by their authors.

## Safety

- View / collect only. No likes, replies, follows, DMs, or posts unless you explicitly approve a draft.
- Engagement helpers (if any) are **beta / hypothesis tests**, not part of the product promise.
- Never store secrets in git.

## Repo map

```
AGENTS.md                 # role card for the desk
ARTICLE.md                # operator case study (English)
config/watchlist.json     # YOUR accounts go here
templates/                # digest + draft rules
examples/                 # redacted sample digest
docs/daily-loop.md        # how a day runs
assets/                   # screenshots for the article / README
```

## License note

Example digests are redacted. Replace with your own scrapes. Third-party posts remain owned by their authors; this repo is a workflow, not a content dump.
