# Daily loop

Content day **D = yesterday** in your configured timezone. Everything on X is **read-only**: the agent fetches with the x MCP connector (or a logged-in read-only browser session) and saves the raw output. Nothing posts, likes, replies, follows or DMs.

## Timeline

1. **~10:00** optional Reddit AI meta (culture heat).
2. **~10:30 collect D.** Watchlist originals of D (no replies, no reposts) with views. Hits ≥ `min_views`, ★ ≥ `star_views`. **Self-quotes count** like any original and only get a `self_quote: true` + `self_quote_label` badge. Only same-text duplicates go to `excluded_hits`. Plus ~20 outsider posts from the operator's niche in the last ~48h, and the last-24h timelines of watchlist accounts (raw files in `digests/<D>/_24h/<handle>.json`). Accounts in `trend_input_only` are fetched too (for example an outsider search `from:<handle>`), but only as trend input.
3. **Build `board/data.json` for D** (hits, virals/outsiders, patterns, no_hits, day_roster, you_rank, leaderboards via `board/enrich_leaderboards.py`).
4. **Prepare the trend layer:** `pipeline/run_day.sh prepare <D>`. It moves trend-input-only posts out of the board lanes, ranks the 24h trend keywords, writes the X keyword search request (16 keywords × 2 windows = 32 searches) and the experiment timeline request, and prints the **TOP-10** posts that need drafts.
5. **Fetch (read-only):** every call in `digests/<D>/_xkw/request.json` with `search_posts_all` (save each raw result as `digests/<D>/_xkw/<file>`), and, when the experiment is on, the one `get_users_posts` call in `digests/<D>/_exp/request.json` (save as `timeline.json`, follow `next_token` as `timeline__p2.json`). Stay under the rate limits.
6. **Drafts v4 (agent writes):** `digests/<D>/_parts/drafts_v4.json` for the TOP-10 only, per [templates/DRAFT_RULES.md](../templates/DRAFT_RULES.md). `python3 pipeline/drafts.py check <D>` must print `rejected=0`.
7. **Ideas (agent writes):** `python3 pipeline/xkw.py ingest <D>` prints the X keyword table. Then write `digests/<D>/_parts/radar_inputs.json` (template: `pipeline/templates/radar_inputs.example.json`): 5-8 post ideas (topic + EN hook + visual + trend keywords, at least 60% built on X-table keywords and at least one from its top 5, never text-only) and 2-3 article ideas.
8. **Run the gates:** `pipeline/run_day.sh <D>`. Drafts check + apply, X keyword ingest, trend radar, experiment, then `digests/<D>/PING.txt`. Exit 3 means a draft or idea was rejected: fix the file it names and re-run.
9. **≤ 12:00 deliver:** send the ping verbatim from `PING.txt` (format in [templates/DIGEST_TEMPLATE.md](../templates/DIGEST_TEMPLATE.md)) plus the digest.
10. **Publish** `board/index.html` + `board/data.json` to **your** GitHub Pages repo (`board/publish-pages.example.sh`). Never the shared demo.
11. The operator picks 1-2 drafts or ideas, edits them and posts them **manually**.

## What the board shows after the run

- **06 / Top hits:** cards with a self-quote badge where relevant, **TOP-10 · #n** badge, why-it-hit line (trend match %, verdict, keywords), draft + keyword chips + 4-gram overlap for TOP-10 only, collapsible original.
- **07b / Trend keywords · 24h:** the ranked keyword list the drafts used.
- **08b / Trends and post ideas:** TOP-10 trend line and summary (real board numbers only), X keyword table (24h vs previous 24h, labelled as a sample), trends 24-48h with heat and momentum, post ideas, article ideas, why-it-hit for every board post (trend / visual / author-audience / coincidence).
- **08c / Experiment:** your own posts in the window, trend vs non-trend, compared inside the same format, against your pre-window median.

Details of every script and field: [docs/pipeline.md](pipeline.md).

## Editing the watchlist

Open `config/watchlist.json` (create it from `config/watchlist.example.json`). Replace handles with whoever is actually viral in **your** niche. Put big aggregator accounts you want as trend signals only into `trend_input_only`. Set `x_keywords.core` to ~16 keywords of your niche. Save. The next run uses the new list. The real watchlist, `board/data.json` and `digests/` are gitignored.

## Your board

See [SETUP.md](SETUP.md), `board/SETUP.md`, and `docs/marketplace-first-run.md`. A filled case-study board (not yours, not the default): https://monkeyteamvip.github.io/kiosa-board/

## Privacy note

Experimental personal tooling. No visitor data collection, no tracking cookies on the board. Reading X is read-only via the operator's own session or connector, never visitor accounts. Not affiliated with X Corp. Third-party posts belong to their authors. No warranty.
