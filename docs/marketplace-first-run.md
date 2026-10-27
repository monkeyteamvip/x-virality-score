# Marketplace first chat

Use this when someone adds the bot from the Grok Bot marketplace, or when they clone the repo and open a first session. The human-readable twin is [first-run.md](first-run.md).

Goal of the first chat: they leave with **their** watchlist file and **their** GitHub Pages URL. https://monkeyteamvip.github.io/kiosa-board/ stays a demo / example for screenshots and the article. Do not save it as their live board, and do not refresh it after their digest.

Do not invent their handle, their accounts, or a Pages URL. Ask, then write.

---

## Stage 0 — Welcome

**What happens.** Open as a creator / blogger desk. They publish. The bot researches and drafts.

**What the user does.** Nothing yet, except stay in the chat.

**What you say.** In a few sentences: watchlist originals above a view floor, keyword / pattern pass, English draft + `video_tip` (Russian only if they set `lang` to `ru`), ~20 outsider posts from their niche in the last ~48 hours, digest before noon, personal board with X Score and Day Target. Point them at `docs/SETUP.md` if they want the written guide.

**Result to expect.** They understand the bot will not auto-post. Ask whether to set up the desk now.

---

## Stage 1 — Collect inputs

**What happens.** You need four facts before any file write.

**What the user does.** Reply with:

1. X handle
2. Timezone (IANA name, such as `America/Los_Angeles`)
3. `min_views` and `star_views` (offer the example defaults `5000` and `10000` if they want them)
4. Watchlist accounts, handles without `@`. Offer `docs/WATCHLIST.md` and `config/examples/` as optional starters. Copy one of those files only after they confirm the handles. Do not treat the example accounts as their list.

**What you do.** Ask for anything missing. Repeat the list back.

**Result to expect.** A confirmed recap. Stop here if they have not answered.

---

## Stage 2 — Write `config/watchlist.json`

**What happens.** Copy `config/watchlist.example.json` to `config/watchlist.json`. The example stays in git with placeholder handles only. The real file is gitignored.

**What the user does.** Confirm the recap, or edit a handle if the recap is wrong.

**What you do.** Write:

```json
{
  "timezone": "America/New_York",
  "min_views": 5000,
  "star_views": 10000,
  "accounts": ["their_handle_one", "their_handle_two"]
}
```

Accounts may also be `{"handle","notes"}` objects. Strip `@` if they included it.

**Result to expect.** The file exists on their machine. `git status` does not show `config/watchlist.json` as a commit. Tell them the path.

---

## Stage 3 — Scaffold the personal board

**What happens.** Start from `board/index.html` + `board/data.example.json`. The UI brands itself from data, not from a hardcoded operator.

**What the user does.** Confirm the display name they want on the board (it can differ from the handle).

**What you do.**

1. `cp board/data.example.json board/data.json`
2. Set `brand_title` (default `Grok Bot X Virality Score` unless they want another title)
3. Set `brand_handle` to `@their_handle`
4. Set `operator.handle`, `operator.name`, and `operator.profile_url` (`https://x.com/their_handle`)
5. Set `ui.default_theme` to `"night"` or `"day"` only if they asked
6. Point them at the Night/Day toggle and [../board/SETUP.md](../board/SETUP.md) for `DASHBOARD_TARGETS` (hits `12`, views `100000`, floors `5000` / `10000` unless they change them)
7. Mention `board/enrich_leaderboards.py` for week/month after digests exist. It reads `operator` from `data.json`. Digest days live under `digests/YYYY-MM-DD/` or `XVS_DIGEST_ROOT`.

**Result to expect.** `board/data.json` is local, gitignored, and shows their handle. A static preview (`python3 -m http.server` inside `board/`) shows that handle in the header. Empty hits are the correct empty state.

---

## Stage 3b — Optional trend layer settings

**What happens.** The daily trend layer (`pipeline/`) works with defaults. A few choices make it theirs.

**What the user does.** Answers, or says "defaults":

1. Any big account (an aggregator) to use as **trend input only**? Its posts feed trend keywords and the radar, never hits, leaderboards or drafts. → `trend_input_only`
2. ~16 niche keywords for the **X keyword table** (24h vs previous 24h, sampled search). → `x_keywords.core` (default: the AI list in the example)
3. Labels and ping in English or Russian? → `lang` (`en` default)
4. Run the **experiment** on their own posts (trend vs non-trend, same-format comparison, vs their pre-window median)? Needs start / end dates and their numeric user id (look it up once, read-only, with `get_users_by_usernames`). → `experiment` (off by default)

**What you do.** Write those keys into `config/watchlist.json`. Do not invent keywords they did not approve beyond the example defaults.

**Result to expect.** A recap of the four choices. The first daily run uses them.

---

## Stage 4 — Publish their Pages URL

**What happens.** Their board becomes a public GitHub Pages site they own.

**What the user does.** Provide their GitHub username and the repo name they want (suggest `x-virality-board`). They need `gh auth login` with repo scope if you run the helper. Do not ask them to paste a token into the repo.

**What you do.** Follow [../board/SETUP.md](../board/SETUP.md):

```bash
export BOARD_OWNER=their-github-user
export BOARD_REPO=x-virality-board
bash board/publish-pages.example.sh
```

The script uploads `index.html` and `data.json` to the root of that repo and requests Pages from `main` `/`.

**Result to expect.** Tell them the exact URL:

`https://<their-github-user>.github.io/<their-repo>/`

Save that URL as the only live board. Say clearly that https://monkeyteamvip.github.io/kiosa-board/ is a demo and is not their dashboard.

If Pages is still building, the result to wait for is that same URL returning the board, not a redirect to the demo.

---

## Stage 5 — Hand off to the daily loop

**What happens.** Later runs read their watchlist, deliver a digest, and refresh the URL from stage 4.

**What the user does.** Keep a logged-in X session on the scraping machine for read-only browsing. Each day, pick 1–2 drafts and post them themselves.

**What you do.** On every digest: regenerate **their** `board/data.json`, run `board/enrich_leaderboards.py` when they want week/month updated, run `pipeline/run_day.sh prepare <D>` → read-only searches → TOP-10 drafts + ideas → `pipeline/run_day.sh <D>`, send the ping from `digests/<D>/PING.txt`, and push `data.json` to **their** Pages repo. Read [daily-loop.md](daily-loop.md) and [pipeline.md](pipeline.md).

Hard stop: never like, reply, repost, follow, DM, delete, or post without a fresh yes for that exact action. Never commit cookies, sessions, or API keys.

**Result to expect.** They can describe tomorrow as: digest in chat, then their `github.io` page shows the new X Score and Day Target.
