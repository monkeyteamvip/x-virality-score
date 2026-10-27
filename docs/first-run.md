# First run — your own X Virality Score desk

The full non-expert guide is [SETUP.md](SETUP.md). Watchlist choices: [WATCHLIST.md](WATCHLIST.md). This page is the same work as a short stage list.

Follow this once after you fork or clone [the repo](https://github.com/monkeyteamvip/x-virality-score). When you finish, you have a private watchlist on your machine and a **public board URL that belongs to you**.

https://monkeyteamvip.github.io/kiosa-board/ is a demo case study. Leave it as a picture of what a finished board can look like. Your daily refresh goes to the Pages URL you create in stage 4.

Agent-side version of this chat: [marketplace-first-run.md](marketplace-first-run.md). Page hosting details: [../board/SETUP.md](../board/SETUP.md).

---

## Stage 0 — Welcome

**What happens.** You get a read-only virality desk: watchlist hits, a keyword / pattern pass, English drafts, video tips, ~20 outsider posts from the last ~48 hours, and a dashboard with X Score and Day Target.

**What you do.** Read the [README](../README.md). If you use Grok Bot, point the agent at this repo (or paste `AGENTS.md`) so the first chat follows [marketplace-first-run.md](marketplace-first-run.md).

**Result you should see.** You can name the six outputs above, and you know you remain the person who posts.

---

## Stage 1 — Say who you are and who you watch

**What happens.** The desk cannot scrape until it has your timezone, view floors, and account list. It also cannot label "YOU" on the board until it has your handle.

**What you do.** Send the agent (or write down):

- your X handle
- timezone, for example `America/New_York` or `Europe/Moscow`
- `min_views` (starter default `5000`) and `star_views` (starter default `10000`)
- watchlist handles **without** `@`

**Result you should see.** A short recap of those four items before any file is written. If something is missing, the agent asks again. It does not invent accounts.

---

## Stage 2 — Write your watchlist

**What happens.** `config/watchlist.example.json` is the committed starter. Placeholders only: `example_account` and `another_handle`. Your real list is a separate file that git ignores.

**What you do.** Read [WATCHLIST.md](WATCHLIST.md) before you fill the list. Optional niche starters live in `config/examples/`.

```bash
cp config/watchlist.example.json config/watchlist.json
```

Edit `accounts`, `timezone`, `min_views`, and `star_views`. Handles have no `@`. This shape is valid too:

```json
{ "handle": "example_account", "notes": "why you watch them" }
```

**Result you should see.** `config/watchlist.json` exists locally and `git status` does not list it as a file to commit. The example file in git still shows only placeholders.

---

## Stage 3 — Scaffold your board

**What happens.** `board/index.html` is a single file (no build). On load it fetches `./data.json` and reads:

- `brand_title`, `brand_handle`
- `operator.handle`, `operator.name`, `operator.profile_url`
- `ui.default_theme` (`"night"` or `"day"`, first visit only)
- `leaderboards.week` / `leaderboards.month`
- `hits`, `outsiders` or `virals`, `patterns`, `no_hits`, `day_roster`, `you_rank`, `previous_day`

The HTML fallback handle is `@your_handle` until `data.json` replaces it. The committed example uses the same placeholders.

**What you do.**

```bash
cp board/data.example.json board/data.json
```

Set `brand_handle`, `operator.handle`, `operator.name`, and `operator.profile_url` to you. Optional: `ui.default_theme`.

Preview with a tiny static server (a `file://` open often blocks `fetch`):

```bash
cd board && python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/`. The header should show your handle from `data.json`. Empty hits are expected before the first digest. Day Target reads NOT DONE until the day's numbers clear the targets in `index.html` (`DASHBOARD_TARGETS`).

**Result you should see.** A local board titled with your brand, Night/Day toggle working, and sections for X Score, Day Target, roster, charts, week/month, hits, outsiders, and no-hits. `board/data.json` stays untracked.

---

## Stage 4 — Publish your GitHub Pages URL

**What happens.** GitHub serves the two board files from a **public repo you own**. The desk stores that URL and uses it after every digest.

**What you do.** Create a public repo (suggested name: `x-virality-board`). Put `index.html` and `data.json` on `main` at the repo root. Enable Pages: Deploy from branch `main` / root.

Or, after `gh auth login` (repo scope; the script contains no token):

```bash
export BOARD_OWNER=your-github-user
export BOARD_REPO=x-virality-board
bash board/publish-pages.example.sh
```

**Result you should see.** This URL loads in a browser after Pages finishes building (often a minute or two):

`https://<your-github-user>.github.io/<your-repo>/`

Copy it into your notes or tell the agent to save it. That string is your live board. The demo URL is not a stand-in while you wait — publish this one, even if the first `data.json` is still the example.

---

## Stage 5 — Daily loop

**What happens.** On later days the desk reads `config/watchlist.json`, scrapes original posts, drafts from mined patterns, and rewrites `board/data.json`. Week/month tables come from `board/enrich_leaderboards.py`, which reads **your** `operator` block (no handle is baked into the script). Then the new `data.json` is pushed to the Pages repo from stage 4.

**What you do.** Keep a logged-in X session on the machine that scrapes. Run the loop in [daily-loop.md](daily-loop.md). Choose 1–2 drafts, edit them, and post them yourself. Approve any like, reply, repost, follow, or DM one action at a time.

**Result you should see.** A digest before noon in your timezone, and your `github.io` board showing that day's X Score, Day Target, and per-hit DONE / NOT DONE chips.

---

## Checklist

- [ ] `config/watchlist.json` has your handles and is gitignored
- [ ] `board/data.json` has your `brand_handle` and `operator`
- [ ] Local preview shows your handle
- [ ] `https://<you>.github.io/<repo>/` is live
- [ ] That URL is the one saved for daily refresh
- [ ] No cookies, tokens, or API keys in git
