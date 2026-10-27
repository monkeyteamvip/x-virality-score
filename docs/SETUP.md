# Set up X Virality Score

This is the full install. The short path is the [Quickstart in the README](../README.md). When you finish, you have a private watchlist on your machine and a public board URL that belongs to you.

You do not need to be a programmer. You do need a GitHub account, an X account, and Python 3 if you want to run the sample or the daily scripts on your own computer.

Two ways to run the same pipeline:

- **Grok Bot (marketplace).** The bot asks for your handle and watchlist, reads public X posts with its built-in X tools, saves the raw results, and runs the scripts in `pipeline/`. You still publish the board and you still post yourself.
- **Standalone.** The Python in `pipeline/` never talks to X. You (or any script) drop the raw JSON into `digests/<date>/`, then `pipeline/run_day.sh` builds the board data and the ping. The sample day is this path with fictional posts.

---

## 1. Get the repo

Pick one:

1. **Fork** on GitHub (Fork button), then clone your fork. Use this if you want your own copy of the code and the history.
2. **Use this template**, if the repository offers "Use this template". You get a new repo without this project's issues and history. Then clone that repo.
3. **Clone** the original if you only want to try it locally:

```bash
git clone https://github.com/monkeyteamvip/x-virality-score.git
cd x-virality-score
```

Confirm the offline sample before you change anything:

```bash
bash scripts/smoke_day.sh
cd board/.smoke-preview && python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/`. Header handle `@your_handle`, English section titles, a Day Target. Ctrl-C stops the server.

`ARTICLE.md` is a case study of one person's desk. It is not the setup, and it is not your board.

## 2. Turn on GitHub Pages

The board is two files: `board/index.html` and `board/data.json`. GitHub Pages serves them. No build step.

Use a **separate public repo** for the board so your watchlist and raw digests never have to be public. Suggested name: `x-virality-board`.

1. Create a new **public** repository under your GitHub user. Leave it empty.
2. Copy `board/index.html` into that repo at the root (not inside a `board/` folder).
3. Copy `board/data.example.json` to `data.json` in that same root, then edit the handle fields in the next section.
4. Settings → Pages → Build and deployment → Deploy from branch → `main` → `/ (root)` → Save.
5. Wait a minute or two. Your URL is:

`https://<your-github-user>.github.io/x-virality-board/`

If the helper is easier and you already ran `gh auth login` (repo scope; do not paste a token into the repo):

```bash
cp board/data.example.json board/data.json
# edit board/data.json first (next section)
export BOARD_OWNER=your-github-user
export BOARD_REPO=x-virality-board
bash board/publish-pages.example.sh
```

Save that URL. The daily loop refreshes this repo only. More on targets and themes: [board/SETUP.md](../board/SETUP.md).

## 3. Set your handle

```bash
cp board/data.example.json board/data.json
cp config/watchlist.example.json config/watchlist.json
```

In `board/data.json` set:

- `brand_title` — the name in the header, for example `Your X Virality Score`
- `brand_handle` — `@your_handle`
- `operator.handle`, `operator.name`, `operator.profile_url` (`https://x.com/your_handle`)
- `timezone` — an IANA name such as `America/New_York`. The starter uses `UTC`.
- optional `ui.default_theme`: `"night"` or `"day"`
- optional `virals_title` — the outsiders heading. The starter says `Outsiders · last 48h`. Set your own label if you want, for example `AI virals · last 48h`.

In `config/watchlist.json` set the same `timezone`, and `experiment.handle` to your handle without `@` if you later turn the experiment on.

Preview again from the repo (a direct `file://` open usually blocks the page from reading `data.json`):

```bash
cd board && python3 -m http.server 8765
```

The header should show your handle. Empty hits are the right empty state before the first real day.

Both real files are gitignored. `git status` should not list them.

## 4. Build your watchlist

Open [WATCHLIST.md](WATCHLIST.md). Short version:

- Add about **15 to 30** accounts that post in your niche and are near your size. A useful ceiling is about **50,000 followers**. Much larger accounts drown the hit list.
- Handles go in `accounts` **without** `@`. A string, or `{"handle": "name", "notes": "why"}`.
- Park giant news bots and aggregators in `trend_input_only`. Their posts still train the keywords. They never become hits, drafts, or leaderboard rows.
- Starter files you can copy from, then edit: `config/examples/`. Every handle in those files was checked on 2026-10-27. Counts go stale. Replace anyone who is the wrong size for you.

Also set:

- `min_views` (starter `5000`) and `star_views` (starter `10000`). The same floors should match `DASHBOARD_TARGETS` in `board/index.html` if you change them. See [board/SETUP.md](../board/SETUP.md).
- `keyword_domain_terms` — lowercase words from your niche that should count as keywords (`agent`, `bitcoin`, `mrr`, ...).
- `x_keywords.core` — about 16 search phrases for the X keyword table. The starter list is an AI example. Niche lists live in `config/examples/`.
- `lang` — `en` or `ru`. English is the default for labels and the ping.
- `board_url` — the Pages URL from section 2. It is printed on the ping.

## 5. Keywords and niche

The keyword table is a **sample**: up to 25 posts per search, last 24 hours vs the previous 24 hours. The board says it is a sample. It is not every post on X.

Pick phrases you would actually search. Ambiguous short words can take a `query_override` so the search is specific. The AI starter does this for `MCP` and `Codex`. Copy that shape:

```json
"query_override": {
  "MCP": "(MCP OR \"MCP server\") (AI OR agent OR server)"
}
```

`keyword_domain_terms` is separate. Those are single lowercase words the ranker is allowed to treat as keywords even when they are not a name or acronym.

## 6. Run the first day

Content day **D** is **yesterday** in your timezone, written `YYYY-MM-DD`.

### With the Grok Bot

Install the bot from the marketplace (or open a chat with this repo's `AGENTS.md`). On the first chat the bot follows [marketplace-first-run.md](marketplace-first-run.md):

1. It asks for your handle, timezone, view floors, and watchlist. It does not invent accounts. You can point it at a file in `config/examples/` and then delete the ones you do not want.
2. It writes `config/watchlist.json` and `board/data.json`.
3. It helps publish the Pages URL and saves that URL as the only board it refreshes.
4. Each day it reads X with the built-in read-only tools (`get_users_posts` for timelines, `search_posts_all` for the keyword table), saves the raw JSON under `digests/<D>/`, and runs `pipeline/run_day.sh`.
5. It sends you the ping from `digests/<D>/PING.txt` verbatim.

The bot does not like, reply, repost, follow, DM, or post unless you say yes to that exact action.

### Standalone

There is no X scraper in this repo. The scripts only read local JSON. A day looks like this:

1. Build `board/data.json` for day D: `hits`, `virals` (outsiders), `patterns`, `no_hits`, `day_roster`, `you_rank`, and `date` set to D. Field shapes are in `board/data.example.json` and the sample in `fixtures/sample-day/data.json`.
2. Optional raw timelines in `digests/<D>/_24h/<handle>.json` (saved `get_users_posts` output).
3. `pipeline/run_day.sh prepare <D>` prints the top-10 posts, writes the keyword search request, and (if the experiment is on) the timeline request.
4. Save each search from `digests/<D>/_xkw/request.json` as the filename that request names. Shape: a JSON object with `data` and `includes.users`, the same shape the X recent-search API returns. The sample files are in `fixtures/sample-day/xkw/`.
5. Write `digests/<D>/_parts/drafts_v4.json` for those top-10 ids, using [templates/DRAFT_RULES.md](../templates/DRAFT_RULES.md). Write `digests/<D>/_parts/radar_inputs.json` from [pipeline/templates/radar_inputs.example.json](../pipeline/templates/radar_inputs.example.json).
6. `pipeline/run_day.sh <D>` checks the drafts, builds the radar, updates `board/data.json`, and writes `digests/<D>/PING.txt`.

`bash scripts/smoke_day.sh` is that sequence with fixtures. Copy it when you want to see the order.

Week and month tables, after you have more than one day:

```bash
python3 board/enrich_leaderboards.py
```

It reads your operator from `board/data.json`. Digest folders default to `digests/`. Override with `XVS_DIGEST_ROOT` if they live somewhere else.

## 7. Read the board

| Section | What it is |
| --- | --- |
| X Score | One number from how many watchlist hits you logged and how many views they have, against the day target in `board/index.html`. |
| Day Target | DONE when both the hit count and the view total clear the targets. Otherwise NOT DONE. |
| Your day | Your best post against the 5k and 10k lines. |
| Daily rank | You and the watchlist, best post / total views. |
| Top hits | Watchlist posts that cleared the floor. Top 10 get a draft you can copy. Each card has a DONE / NOT DONE chip. |
| Trend keywords | The ranked 24h list the drafts used. |
| Outsiders | Posts from outside the watchlist, last ~48h. The heading comes from `virals_title`. |
| Trends and post ideas | Why each post hit, the keyword sample table, ideas, article ideas. |
| Experiment | Only after you turn `experiment.enabled` on. Your posts, trend vs non-trend, same format, against your earlier median. |

Copy a draft, edit it, and post it yourself. One or two posts a day is the point.

## 8. Daily routine

Follow [daily-loop.md](daily-loop.md). In short, around late morning in your timezone:

1. Collect yesterday's originals and outsider posts.
2. `pipeline/run_day.sh prepare <D>`, then the read-only searches, then the drafts and ideas.
3. `pipeline/run_day.sh <D>`.
4. Send yourself `digests/<D>/PING.txt` unchanged.
5. Upload the new `data.json` (and `index.html` if it changed) to **your** Pages repo.

A ping in English looks like this:

```text
X digest 26.10: 4 hits ≥5k (3 ★) (self-quotes: 1); +2 outsiders.
X keywords 24h (sample): top-5 Claude Code 23.0K ↑, prompt injection 18.0K ↑
TOP-10: 6/6 (100%) matched trends · trend 6
Experiment @your_handle 2026-10-21..2026-10-26: 2 posts; trend n=1 3.0x vs non-trend n=1 1.0x · +200%
Board: https://your-github-user.github.io/x-virality-board/
```

The experiment line is omitted when the experiment is off. The self-quote phrase is omitted when the count is zero. With `"lang": "ru"` the same lines are Russian. The template is in [templates/DIGEST_TEMPLATE.md](../templates/DIGEST_TEMPLATE.md).

## 9. Optional experiment

In `config/watchlist.json`, `experiment.enabled` is `false` until you fill it in.

- `handle` — yours, without `@`
- `user_id` — the numeric id from a one-time read-only user lookup
- `start` and `end` — `YYYY-MM-DD`, in your timezone
- `hypothesis` — one sentence the board shows
- Leave `trend_threshold` at `35`, `min_n` at `5`, and `min_age_h` at `24` unless you know why you are changing them

The board says "sample too small" until each group has enough posts. Compare video with video and image with image. That is the fair row.

## 10. Troubleshooting and FAQ

**The page says it failed to load data.json.** You opened the HTML as a file. Run `python3 -m http.server` inside the folder that contains both `index.html` and `data.json`.

**The header still says @your_handle.** `data.json` is missing, or the page is still reading the example. Edit `brand_handle` and `operator`, then reload.

**`missing config/watchlist.json`.** Copy `config/watchlist.example.json` to `config/watchlist.json`.

**`run_day.sh` exits 3.** A draft or an idea was rejected, or the keyword search files are missing. The error names the file. Rules: [templates/DRAFT_RULES.md](../templates/DRAFT_RULES.md). Re-run the same command after you fix that file.

**No hits.** Normal when nobody on the list cleared `min_views`. The No-hits section should say why. If the list is full of huge aggregators, move them to `trend_input_only` and add peers. See [WATCHLIST.md](WATCHLIST.md).

**An aggregator showed up as a hit.** The handle in `trend_input_only` does not match (extra `@` is fine; a typo is not). Fix it and run `python3 pipeline/trend_input.py <D>`.

**Pages URL 404.** The repo is private, Pages is still building, or `index.html` is not at the repo root. Give it two minutes, then check Settings → Pages.

**The ping is in Russian.** `lang` is `ru`. Set `lang` to `en` and re-run `pipeline/run_day.sh <D>` so the radar line is rebuilt in English. The ping script and the radar both read `lang` when they run.

**Git wants to commit my watchlist or digests.** Those paths are gitignored. Do not force-add them. Never commit cookies, sessions, or API keys.

**Can I track a niche that is not AI?** Yes. Replace `x_keywords.core`, `keyword_domain_terms`, and the watchlist. The outsiders heading is `virals_title` in `data.json`.

**Does the sample day call X?** No. `bash scripts/smoke_day.sh` uses `fixtures/sample-day/` only. It also checks that the starter config stays a placeholder and that English is the default.
