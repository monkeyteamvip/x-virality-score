# Marketplace / first chat

When someone adds this bot from the Grok Bot marketplace (or clones the repo), the **first conversation** should:

1. Welcome them as a creator/blogger desk (not an auto-poster)
2. Ask for: their **X handle**, timezone, `min_views`, and **watchlist accounts**
3. Write `config/watchlist.json`
4. Scaffold a personal board from `board/` (`index.html` + `data.json` with their `brand_handle`)
5. Offer to publish **their** GitHub Pages board (`board/SETUP.md` / `publish-pages.example.sh`)
6. Save their Pages URL as the only live board for daily refresh
7. Label https://monkeyteamvip.github.io/kiosa-board/ as demo/example only

Daily after digests: refresh **their** `data.json` and push to **their** Pages repo.
