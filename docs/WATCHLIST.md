# Choosing your watchlist

The watchlist is the product. A good list is people your size who post original work in your niche. A bad list is a pile of news bots. Their numbers are not yours, and they fill every leaderboard.

Edit `config/watchlist.json` (copy it from `config/watchlist.example.json`). Handles have no `@`.

## Who to add

- **Peers.** Same niche, posting originals most days, roughly your follower count. If you are unsure, stay at or under about **50,000 followers**. A 500,000-follower account will "win" every day and teach you less than someone who posts the way you can post.
- **Active.** You want originals that can clear `min_views` (starter: 5,000). A silent account only shows up under No hits.
- **How many.** About **15 to 30**. Under 15, one lucky post swings the day. Over 30, the morning collect gets long and the keyword list gets muddy.
- **You.** Your own handle belongs on the board (`operator` in `board/data.json`), and in `experiment.handle` if you run the experiment. You do not have to put yourself in `accounts` unless you want your posts scored as watchlist hits too.

An account can be a plain string or an object:

```json
{"handle": "example_account", "notes": "why you watch them"}
```

## Who to leave out of the hit list

Giant aggregators, link roundups, and "whale alert" style bots post all day. They skew hit counts, keyword ranks, and the top-10 drafts.

Put those handles in `trend_input_only`:

```json
"trend_input_only": ["example_aggregator"]
```

The desk still fetches them, and their text can feed keywords and the trend radar. They are never shown as hits, outsiders, leaderboard rows, or drafts.

Do the same for any single famous account that is far bigger than you, if their posts would otherwise dominate the board. You can always move them back later.

## Starter files

These are optional starting points, not your list until you say so. Copy one over `config/watchlist.json`, delete anyone you do not want, and add peers you actually read.

| Niche | File |
| --- | --- |
| AI and dev tools | [config/examples/ai-dev-tools.json](../config/examples/ai-dev-tools.json) |
| Crypto | [config/examples/crypto.json](../config/examples/crypto.json) |
| Indie hackers and SaaS | [config/examples/indie-hackers.json](../config/examples/indie-hackers.json) |
| Marketing and creators | [config/examples/marketing-creators.json](../config/examples/marketing-creators.json) |

Every handle in those files was a public X account on **2026-10-27**, looked up with a public user search. The notes include a rounded follower count from that day. Counts move. If a name is much larger than you, move it to `trend_input_only` or delete it.

The crypto file has one smaller account in `accounts` and the well-known large accounts in `trend_input_only`. The public crypto names that came up in search were far above 50,000 followers. Add your own peers in that gap. Do not paste in extra handles you have not checked.

The default file everyone starts from is still `config/watchlist.example.json`: placeholders only (`example_account`, `another_handle`), timezone `UTC`, language `en`.

## Keywords that match the list

Each starter file also fills `x_keywords.core` (about 16 search phrases) and `keyword_domain_terms` (lowercase words the ranker may keep). Change both when you change niche. Details: [SETUP.md](SETUP.md) and [pipeline.md](pipeline.md).
