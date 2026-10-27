# Set up your own board

Every fork and every marketplace import gets a **personal** dashboard. The files in this folder are the starter. Your live site is the GitHub Pages URL you publish below.

https://monkeyteamvip.github.io/kiosa-board/ is a case-study demo you can open to see a filled-in board. Your digests update the URL from section 5, which is yours.

Schema for the JSON the page reads: `board/data.example.json` (same fields the UI uses: `brand_title`, `brand_handle`, `operator`, `ui.default_theme`, `leaderboards`, `hits`, `day_roster`, `you_rank`, and the rest of that file).

Sections added by the trend pipeline (`pipeline/`, see `docs/pipeline.md`) appear only when their data exists: TOP-10 badges + drafts with keyword chips and overlap (`top10_rank`, `draft_en`, `draft_keywords`, `draft_check`, `original_en`), self-quote badge (`self_quote`, `self_quote_label`), why-it-hit line (`why_hit`), **07b Trend keywords** (`trend_keywords`), **08b Trends and post ideas** (`trend_radar`, incl. the X keyword table) and **08c Experiment** (`experiment`).

---

## 1. Brand and watchlist

**What happens.** The page title and the YOU chip come from `data.json`. The scrape list comes from the watchlist.

**What you do.**

- Copy `config/watchlist.example.json` to `config/watchlist.json` and replace the placeholder handles.
- Copy `board/data.example.json` to `board/data.json` and set:
  - `brand_title` — header title (default in the example: `Your X Virality Score`; the page also accepts `Grok Bot X Virality Score`)
  - `brand_handle` — shown next to the title, for example `"@you"`
  - `operator.handle` / `operator.name` / `operator.profile_url` — YOU highlighting on the roster and leaderboards
  - `timezone` — label in the header meta line
  - optional `ui.default_theme`: `"night"` or `"day"` (first visit only; a visitor's toggle wins via `localStorage` key `xvs-theme`)
  - optional `virals_title` — outsiders heading. The page defaults to `Outsiders · last 48h` when this is omitted. Set it if you want a niche label.

**Result you should see.** `data.json` names you. Both real files are gitignored (see the repo `.gitignore`).

---

## 2. Targets (hits / views / floors)

**What happens.** Day Target DONE / NOT DONE uses four numbers in `board/index.html`, not the JSON file.

**What you do.** Edit:

```js
const DASHBOARD_TARGETS = Object.freeze({
  hits: 12,          // watchlist hits for day target
  views: 100000,     // total views for day target
  minHitViews: 5000, // HIT floor / vs 5k bar
  starViews: 10000   // ★ highlight / vs 10k bar
});
```

Align `min_views` / `star_views` in `config/watchlist.json` with the same floors.

**Result you should see.** The Day Target bars and the per-hit chips use your numbers after you reload.

---

## 3. Preview locally

**What happens.** `index.html` fetches `./data.json` (relative, cache-busted). Opening the file directly often blocks that fetch.

**What you do.**

```bash
cp board/data.example.json board/data.json
# edit brand_* / operator / ui.default_theme
cd board && python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/`.

**Result you should see.** Header handle matches `brand_handle`. X Score, Day Target, day roster (best/total), charts, week/month boards, hits, outsiders, and no-hits all render. An empty `hits` array shows the empty state, which is correct before the first digest.

---

## 4. After each digest

**What happens.** The day's digest replaces the arrays inside `board/data.json` (hits, views, drafts, outsiders, roster, leaderboards). Brand fields stay.

**What you do.** Regenerate `board/data.json`. Keep `brand_title`, `brand_handle`, `operator`, and optional `ui`.

Week and month boards:

- Persist daily slices in `board/leaderboard_ledger.json` (gitignored).
- Upsert that day into the ledger, then recompute week (rolling 7) and month (calendar month from `tracking_start`). Rolling the week window does not reset the month.
- Run `python3 board/enrich_leaderboards.py`.
- The script reads your operator from `data.json`. Point it at digest folders with `XVS_DIGEST_ROOT` if they are not in `digests/YYYY-MM-DD/` next to the repo. Optional env: `XVS_DATA`, `XVS_LEDGER`, `XVS_WATCHLIST`, `XVS_TRACKING_START`, `XVS_TIMEZONE`, `XVS_MIN_VIEWS`, `XVS_OPERATOR_HANDLE`, `XVS_OPERATOR_NAME`.

**Result you should see.** `leaderboards.week.label` and `leaderboards.month.label` show different ranges, and your handle is the YOU row when that day cleared the view floor.

---

## 5. Publish your GitHub Pages site

**What happens.** GitHub hosts `index.html` and `data.json` from a public repo you own. No build step.

**What you do.**

1. Create a **public** repo under your account (suggested name: `x-virality-board`).
2. Put `index.html` and `data.json` on `main` at the repo root.
3. Enable GitHub Pages: Deploy from branch `main` / root.
4. Your URL: `https://<your-github-user>.github.io/x-virality-board/`

Helper (no secrets in the file; you need `gh auth login` with repo scope):

```bash
export BOARD_OWNER=your-github-user
export BOARD_REPO=x-virality-board
bash board/publish-pages.example.sh
```

**Result you should see.** That `github.io` URL loads your board after Pages builds. Save it. Daily refreshes upload a new `data.json` to this repo.

---

## 6. Demo link

**What happens.** The project keeps one public example so articles and newcomers can see a populated board.

**What you do.** Open it if you want a visual reference:

https://monkeyteamvip.github.io/kiosa-board/

**Result you should see.** A finished-looking board that is **not** wired to your watchlist. Your URL from section 5 is the one that changes after your digests.

---

## Board UI features

- Token-driven Night / Day themes (toggle + `localStorage`; first visit respects `prefers-color-scheme`, then optional `ui.default_theme`)
- Count-up metrics, LIVE SIGNAL pulse, ambient grid drift + soft noise (honors `prefers-reduced-motion`)
- SVG charts: top-hit sparkline + day-compare bars + week coverage strip (no chart libraries)
- Staggered card entrance + hover micro-interactions
- Week + Month leaderboards from `leaderboards` in `data.json` (best / total)
- Daily rank roster with best / total and a YOU chip
- No-hits block with `@handles` and `reason` / `max_views`
- Single-file HTML (inline CSS + JS)
- Phone and tablet layout pass (`xvs-mobile-2026`)
