# Public board

## Personal board (every importer)

Each operator gets **their own** GitHub Pages dashboard. Full guide: [SETUP.md](SETUP.md). Stage list: [first-run.md](first-run.md).

1. First chat: collect X handle + watchlist → write `config/watchlist.json` (gitignored; start from `watchlist.example.json`)
2. Scaffold from repo `board/` (`data.example.json` → gitignored `data.json`, with their `brand_handle` and `operator`)
3. Publish to **their** `https://<user>.github.io/<repo>/` URL
4. Refresh that board after every daily digest

**Result:** the URL in step 3 loads their X Score and Day Target. That URL is the one saved for the daily loop.

## Demo / example only

https://monkeyteamvip.github.io/kiosa-board/

Source: https://github.com/monkeyteamvip/kiosa-board

This is a **reference** board for articles and demos. Do **not** point new marketplace importers at it as their live board.

## Notes

Do not use ephemeral trycloudflare tunnels for the durable public URL.
