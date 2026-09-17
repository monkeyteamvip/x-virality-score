# Set up YOUR own board

Every marketplace import / repo fork gets a **personal** dashboard. Do not use someone else's demo board as yours.

## 1. Brand + watchlist

- Set your X handle and accounts in `config/watchlist.json`
- In `board/data.json` set `brand_title` and `brand_handle` (e.g. `"@you"`)

## 2. Local board files

```bash
cp board/data.example.json board/data.json
# edit brand_* fields
# open board/index.html locally (needs a tiny static server if file:// blocks fetch)
```

`index.html` loads `./data.json` and shows X Score, Day Target, and hits.

## 3. After each digest

Regenerate `board/data.json` from that day's digest (hits, views, drafts, outsiders). Keep `brand_title` / `brand_handle`.

## 4. Publish YOUR GitHub Pages

1. Create a **public** repo under your account (suggested name: `x-virality-board`)
2. Put `index.html` + `data.json` on `main` at the repo root
3. Enable GitHub Pages: Deploy from branch `main` / root
4. Your URL: `https://<your-github-user>.github.io/x-virality-board/`

Example helper (no secrets):

```bash
export BOARD_OWNER=your-github-user
export BOARD_REPO=x-virality-board
bash board/publish-pages.example.sh
```

## 5. Demo link (not yours)

https://monkeyteamvip.github.io/kiosa-board/ is a **case-study demo** only. Importers must publish their own Pages URL.

## Board UI features

- Count-up metrics on load/refresh
- LIVE SIGNAL pulse in the header
- Small CSS/SVG Grok Bot ambient animation (honors `prefers-reduced-motion`)
- Day / Night theme toggle (`localStorage` key `xvs-theme`)
- Week + Month leaderboards from `leaderboards` in `data.json`
- No-hits block with prominent `@handles` and `reason` / `max_views`

See the live demo schema on https://monkeyteamvip.github.io/kiosa-board/ (`data.json`).
