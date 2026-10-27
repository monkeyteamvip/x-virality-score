# Trend pipeline (v4/v5)

Stdlib-only Python in `pipeline/`. It reads and writes local JSON only and never talks to X. The agent does the read-only fetches and saves raw tool output into `digests/<D>/`.

Paths (env overrides): `XVS_DIGEST_ROOT` (default `digests/`), `XVS_DATA` (default `board/data.json`), `XVS_WATCHLIST` (default `config/watchlist.json`).

| Script | What it does | Writes |
| --- | --- | --- |
| `run_day.sh prepare <D>` | trend-input split, trend keywords, X keyword request, experiment request, prints TOP-10 | `_parts/trend_keywords.json`, `_xkw/request.json`, `_exp/request.json`, `_parts/originals.json` |
| `run_day.sh <D> [--skip-drafts]` | all gates, then ping | `board/data.json`, `PING.txt` |
| `trend_input.py <D>` | moves posts of `trend_input_only` accounts out of hits / virals / roster / no_hits / leaderboards into `trend_input_only_posts` | `board/data.json` |
| `drafts.py keywords <D>` | ranks last-24h keywords from hits, outsiders, trend-input posts, last-24h posts ≥ `min_views`, `_24h/*.json`, the pattern brief | `_parts/trend_keywords.json` (`extra` / `exclude` curation survives re-runs) |
| `drafts.py top10 <D>` | the 10 most-viewed board posts | `_parts/originals.json` |
| `drafts.py check <D>` | Draft rules v4 gate (4-gram > 30%, copied run ≥ 7, dashes, keywords, new numbers, reply openers) | exit 1 on reject |
| `drafts.py apply <D>` | patches `draft_en`, `draft_keywords`, `draft_check`, `top10_rank`, `original_en`, `board_rank`, `drafts_top10`, `trend_keywords`; removes drafts outside the TOP-10 | `board/data.json` |
| `xkw.py request/ingest <D>` | X keyword table: ~16 keywords, last 24h vs previous 24h, 25-post relevancy **sample** per window | `_xkw/request.json`, `_xkw/keywords.json` |
| `radar.py build <D>` | trends 24/48h, why-it-hit per board post, summary + TOP-10 trend line, validates ideas / articles | `data.json.trend_radar`, per-card `why_hit` |
| `experiment.py request/build <D>` | operator posts in the window, trend vs non-trend, same-format comparison, pre-window median baseline | `data.json.experiment`, `digests/_experiment.json` |
| `ping.py <D>` | the ping text | `PING.txt` |

## Config keys (`config/watchlist.json`)

- `trend_input_only`: handles used only as trend signals (e.g. a big aggregator).
- `lang`: `en` (default) or `ru` for verdict labels and the ping. English is what a new install produces. Set `ru` only when Russian labels are wanted, then re-run the day so the radar line is rebuilt in that language.
- `virals_title` on `board/data.json` (optional): outsiders section heading. Omitted, the page shows `Outsiders · last 48h`.
- `keyword_domain_terms`: lowercase niche words that count as keywords.
- `x_keywords`: `core` (~16 keywords), `query_override`, `max`.
- `experiment`: `enabled`, `handle`, `user_id`, `start`, `end`, `baseline_days`, `trend_threshold` (35), `min_n` (5), `min_age_h` (24), `hypothesis`.
- `board_url`: your Pages URL, printed in the ping.

## Scoring

- **Trend match (why it hit):** `1 - Π(1 - w)` over matched 24h keywords that another author also used (w: rank 1-10 0.35, 11-25 0.22, 26-40 0.12, curated 0.20). Verdict: ≥ 50% trend → video/image visual → ≥ 100K followers (or ≥ 500K views when followers are unknown, an estimate) author/audience → coincidence/other. Missing data shows as "no data".
- **Trend vs non-trend summary:** counts, medians and means from board numbers only.
- **Experiment:** strict trend match uses only keywords known **before** the post (the latest run's `trend_keywords.json` created before `posted_at` + that run's X table), specific keywords only (phrases, names, acronyms, versions), label trend at ≥ 35%. `x_base` = views / median of your originals in the `baseline_days` before `start`. Totals only use posts ≥ 24h old; "sample too small" until n ≥ 5 per group. Read the per-format rows (video vs video, image vs image) for the fair comparison.

## Raw file layout

```
digests/<D>/
  _24h/<handle>.json          raw get_users_posts, last 24h (optional; __p2 for pages)
  _xkw/request.json           written by xkw.py request
  _xkw/<keyword>__24h.json    raw search_posts_all (agent)
  _xkw/<keyword>__prev24h.json
  _xkw/candidates_extra.json  optional extra keywords (JSON list)
  _exp/request.json           written by experiment.py request
  _exp/timeline.json          raw get_users_posts (agent)
  _parts/trend_keywords.json  drafts.py keywords
  _parts/originals.json       drafts.py top10
  _parts/drafts_v4.json       agent
  _parts/radar_inputs.json    agent
  PING.txt                    ping.py
```
