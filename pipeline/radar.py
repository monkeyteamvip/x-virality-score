#!/usr/bin/env python3
"""Trends and post ideas (trend radar) -> board/data.json["trend_radar"] for content day D.

  radar.py build <D> [--no-ideas-ok]

Inputs (local only, read-only on X):
  board/data.json                       hits, excluded_hits, virals/outsiders, trend_input_only_posts, last24h
  digests/<D>/_24h/*.json               raw last-24h timelines (optional)
  digests/<D>/_parts/trend_keywords.json  ranked 24 h keywords (drafts.py keywords)
  digests/<D>/_xkw/keywords.json        X keyword table (xkw.py ingest), embedded as trend_radar.x_keywords
  digests/<D>/_parts/radar_inputs.json  WRITTEN BY THE AGENT each day (template: pipeline/templates/radar_inputs.example.json)
      {"topics":   [{"name", "keywords": [...]}],     optional; auto-clustered if absent
       "ideas":    5-8 x {"title", "hook_en", "angle", "topic", "keywords", "format", "why",
                          "visual_type": video|screencast|image|meme|carousel, "visual"}   (no text-only ideas)
       "articles": 2-3 x {"title", "thesis", "outline": [3-7], "keywords", "visual", "why"},
       "takeaway": "..."}                             optional override of the computed one-liner (real numbers only)

Sections: summary (incl. "TOP-10: x/10 (y%) matched trends"), A) trends 24 h / 48 h (heat, momentum,
evidence), X keyword table, B) post ideas, B2) article ideas, C) why it hit (per board post).
Exit 3 = RADAR REJECTED (the message lists what to fix).
"""
from __future__ import annotations

import glob
import json
import math
import re
import statistics
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

from common import (BANNED_DASHES, board_posts, canon, clean, day_dir, labels, load_config, load_data, load_raw,
                    post_id, record_text, save_data, thresholds)

VISUALS = {"video", "screencast", "image", "meme", "carousel"}   # every idea carries one (no text-only posts)
BIG_ACCOUNT = 100_000
TREND_CUT = 50          # why-it-hit: trend verdict at >= 50 % trend match
MEGA_VIEWS = 500_000    # outsiders have no follower data: >= 500K views -> author/audience (estimate)


def ts(s):
    try:
        t = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def kw_re(k):
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(k) + r"(?:s|es)?(?![A-Za-z0-9])", re.I)


def media_kind(r):
    m = str(r.get("media") or r.get("media_note") or "").lower()
    if not m:
        return None
    if "video" in m or "gif" in m:
        return "video"
    if "image" in m or "photo" in m:
        return "image"
    return "text"


def fmt(n):
    return "-" if n is None else f"{n/1e6:.2f}M" if n >= 1e6 else f"{n/1e3:.1f}K" if n >= 1e3 else str(n)


def corpus(D, d, floor):
    posts = {}

    def add(r, lane):
        i = post_id(r)
        if not i:
            return
        if i in posts:
            return
        fol = (r.get("followers") or {}).get("count") if isinstance(r.get("followers"), dict) else r.get("followers_count")
        text = re.sub(r"@(?=[A-Za-z])", "", record_text(r))
        posts[i] = {"id": i, "handle": r.get("handle"), "url": r.get("url") or r.get("status_url"),
                    "views": int(r.get("views") or 0), "posted_at": r.get("posted_at"), "text": text,
                    "hook": (r.get("hook") or text.split("\n")[0])[:160], "media": media_kind(r),
                    "followers": fol, "lane": lane}
    for lane, r in board_posts(d):
        add(r, lane)
    for r in d.get("excluded_hits") or []:
        add(r, "watchlist")
    for r in d.get("trend_input_only_posts") or []:
        add(r, "trend_input")
    for r in (d.get("last24h") or {}).get("posts") or []:
        add(r, "24h")
    for f in glob.glob(str(day_dir(D) / "_24h" / "*.json")):
        key = "@" + re.sub(r"__p\d+$", "", Path(f).stem)
        for p in load_raw(f).get("data") or []:
            add({"id": p["id"], "handle": key, "views": (p.get("public_metrics") or {}).get("impression_count"),
                 "posted_at": p.get("created_at"),
                 "text": clean((p.get("note_tweet") or {}).get("text") or p.get("text") or "")}, "24h")
    return {k: v for k, v in posts.items() if v["views"] >= floor}


def auto_topics(posts, kws, n=7):
    occ = {k: {i for i, p in posts.items() if k in p["kw"]} for k, _ in kws}
    occ = {k: s for k, s in occ.items() if len(s) >= 2}
    used, out = set(), []
    for k, _ in kws:
        if k not in occ or k in used:
            continue
        mem = [k] + [o for o in occ if o != k and o not in used
                     and len(occ[o] & occ[k]) >= 0.4 * min(len(occ[o]), len(occ[k]))][:5]
        used |= set(mem)
        out.append({"name": " / ".join(mem[:2]), "keywords": mem})
        if len(out) >= n:
            break
    return out


def build(D: str, need_ideas=True):
    cfg = load_config()
    L = labels(cfg)
    ru = str(cfg.get("lang") or "en").lower() == "ru"
    floor, _ = thresholds(cfg)
    d = load_data()
    if d.get("date") != D:
        sys.exit(f"data.json date {d.get('date')} != {D}")
    day = day_dir(D)
    tk = json.loads((day / "_parts" / "trend_keywords.json").read_text())
    kws = [(r["keyword"], r["rank"]) for r in tk["keywords"]]
    kws += [(x, None) for x in tk.get("extra", []) if x.lower() not in {k.lower() for k, _ in kws}]
    inp_p = day / "_parts" / "radar_inputs.json"
    inp = json.loads(inp_p.read_text()) if inp_p.exists() else {}
    end = ts((d.get("last24h") or {}).get("end")) or ts(d.get("updated")) or datetime.now(timezone.utc)
    s24, s48 = end - timedelta(hours=24), end - timedelta(hours=48)
    posts = corpus(D, d, floor)
    for p in posts.values():
        t = ts(p["posted_at"])
        p["bucket"] = None if not t else ("24h" if s24 <= t <= end else "48h" if s48 <= t < s24 else "older")
        p["kw"] = [k for k, _ in kws if kw_re(k).search(p["text"])]
    authors = {}
    for p in posts.values():
        for k in p["kw"]:
            authors.setdefault(k, set()).add(canon(p["handle"]))
    rank = dict(kws)

    def w(k):
        r = rank.get(k)
        return 0.20 if r is None else 0.35 if r <= 10 else 0.22 if r <= 25 else 0.12

    # ---- A) topics 24 h / 48 h
    topics = []
    for t in inp.get("topics") or auto_topics(posts, kws):
        res = [kw_re(k) for k in t["keywords"]]
        m = [p for p in posts.values() if p["bucket"] in ("24h", "48h") and any(r.search(p["text"]) for r in res)]
        if not m:
            continue
        h24 = sum(math.log10(p["views"]) for p in m if p["bucket"] == "24h")
        hprev = sum(math.log10(p["views"]) for p in m if p["bucket"] == "48h")
        if hprev == 0:
            mom = "new · 24 h only"
        elif h24 == 0:
            mom = "down · previous 24 h only"
        else:
            ratio = h24 / hprev
            mom = (f"up x{ratio:.2f}" if ratio >= 1.3 else f"cooling x{ratio:.2f}" if ratio <= 0.7 else f"steady x{ratio:.2f}")
        used = sorted({k for p in m for k in t["keywords"] if kw_re(k).search(p["text"])},
                      key=lambda k: -sum(1 for p in m if kw_re(k).search(p["text"])))
        v24 = sum(p["views"] for p in m if p["bucket"] == "24h")
        v48 = sum(p["views"] for p in m if p["bucket"] == "48h")
        topics.append({"name": t["name"], "keywords": used[:8], "posts_24h": sum(1 for p in m if p["bucket"] == "24h"),
                       "posts_48h": len(m), "views_24h": v24, "views_prev24h": v48, "views_48h": v24 + v48,
                       "momentum": mom, "heat_raw": round(h24 + 0.5 * hprev, 2),
                       "evidence": [{"handle": p["handle"], "views": p["views"], "url": p["url"], "hook": p["hook"],
                                     "lane": p["lane"]} for p in sorted(m, key=lambda p: -p["views"])[:3]]})
    mx = max((t["heat_raw"] for t in topics), default=1) or 1
    for t in topics:
        t["heat"] = round(100 * t["heat_raw"] / mx)
    topics.sort(key=lambda t: -t["heat"])

    # ---- C) why it hit (every board post: watchlist hits + outsiders)
    def judge(r, lane):
        p = posts.get(post_id(r)) or {"kw": [], "text": record_text(r)}
        kwp = [k for k in p.get("kw", []) if len(authors.get(k, set()) - {canon(r.get("handle"))}) >= 1]
        score = round(100 * (1 - math.prod(1 - w(k) for k in kwp))) if kwp else 0
        med = media_kind(r)
        fol = (r.get("followers") or {}).get("count") if isinstance(r.get("followers"), dict) else r.get("followers_count")
        if score >= TREND_CUT:
            v = L["trend"]
        elif med in ("video", "image"):
            v = L["visual"]
        elif fol and fol >= BIG_ACCOUNT:
            v = L["author"]
        elif fol is None and int(r.get("views") or 0) >= MEGA_VIEWS:
            v = L["author"]
        else:
            v = L["other"]
        note = []
        if med is None:
            note.append(f"media: {L['no_data']}")
        if fol is None:
            note.append(f"followers: {L['no_data']}" + (" (estimate from reach >= 500K)" if v == L["author"] else ""))
        top_topic = next((t["name"] for t in topics if any(kw_re(k).search(p.get("text", "")) for k in t["keywords"])), None)
        return {"id": post_id(r), "handle": r.get("handle"), "lane": lane, "views": int(r.get("views") or 0),
                "trend_match": score, "verdict": v, "matched_keywords": kwp[:10], "media": med or L["no_data"],
                "followers": fol, "topic": top_topic, "self_quote": bool(r.get("self_quote")), "note": ", ".join(note)}

    why = []
    for lane, r in board_posts(d):
        j = judge(r, lane)
        why.append(j)
        r["why_hit"] = {k: j[k] for k in ("trend_match", "verdict", "matched_keywords", "media", "note", "topic")}

    # ---- summary (real board numbers only)
    def stats(rows):
        tr = [x["views"] for x in rows if x["verdict"] == L["trend"]]
        nt = [x["views"] for x in rows if x["verdict"] != L["trend"]]
        return {"n": len(rows), "trend_n": len(tr), "trend_pct": round(100 * len(tr) / len(rows)) if rows else 0,
                "avg_trend": round(statistics.mean(tr)) if tr else None, "avg_other": round(statistics.mean(nt)) if nt else None,
                "median_trend": round(statistics.median(tr)) if tr else None,
                "median_other": round(statistics.median(nt)) if nt else None,
                "verdicts": {v: sum(1 for x in rows if x["verdict"] == v)
                             for v in (L["trend"], L["visual"], L["author"], L["other"])}}
    S = {"all": stats(why), "watchlist": stats([x for x in why if x["lane"] == "watchlist"]),
         "outsiders": stats([x for x in why if x["lane"] == "outsider"]),
         "top10": stats(sorted(why, key=lambda x: -x["views"])[:10])}
    vid = [x["views"] for x in why if x["media"] == "video"]
    novid = [x["views"] for x in why if x["media"] in ("text", "image")]
    S["media"] = {"video_n": len(vid), "median_video": round(statistics.median(vid)) if vid else None,
                  "other_n": len(novid), "median_other": round(statistics.median(novid)) if novid else None}
    a, wl, t10 = S["all"], S["watchlist"], S["top10"]
    vbreak = ", ".join(f"{k} {v}" for k, v in sorted(t10["verdicts"].items(), key=lambda kv: -kv[1]) if v)
    if ru:
        top10_line = f"Топ-10: {t10['trend_n']}/{t10['n']} ({t10['trend_pct']}%) совпали с трендами · {vbreak}"
        headline = (f"Из {a['n']} хитов на борде {a['trend_n']} ({a['trend_pct']}%) совпали с трендами 24-48 ч. "
                    f"Медиана просмотров: трендовые {fmt(a['median_trend'])} vs остальные {fmt(a['median_other'])} "
                    f"(среднее {fmt(a['avg_trend'])} vs {fmt(a['avg_other'])}). Watchlist: {wl['trend_n']}/{wl['n']} в тренде. "
                    f"С видео {len(vid)} хитов, медиана {fmt(S['media']['median_video'])} vs без видео {fmt(S['media']['median_other'])}.")
    else:
        top10_line = f"TOP-10: {t10['trend_n']}/{t10['n']} ({t10['trend_pct']}%) matched trends · {vbreak}"
        headline = (f"{a['trend_n']} of {a['n']} board hits ({a['trend_pct']}%) matched 24-48 h trends. "
                    f"Median views: trend {fmt(a['median_trend'])} vs non-trend {fmt(a['median_other'])} "
                    f"(mean {fmt(a['avg_trend'])} vs {fmt(a['avg_other'])}). Watchlist: {wl['trend_n']}/{wl['n']} on trend. "
                    f"{len(vid)} hits with video, median {fmt(S['media']['median_video'])} vs {fmt(S['media']['median_other'])} without.")
    if inp.get("takeaway"):
        take = inp["takeaway"]
    else:
        top = topics[0]["name"] if topics else "-"
        if wl["median_trend"] and wl["median_other"] and wl["median_trend"] > wl["median_other"]:
            take = (f"Trend posts won on the watchlist ({fmt(wl['median_trend'])} vs {fmt(wl['median_other'])} median): "
                    f"put the keywords of the top radar topic in the first line ({top}).")
        elif S["media"]["median_video"] and S["media"]["median_other"] and S["media"]["median_video"] > S["media"]["median_other"]:
            take = (f"Video beat no-video ({fmt(S['media']['median_video'])} vs {fmt(S['media']['median_other'])} median): "
                    f"take the top radar topic and package it as a video or screencast ({top}).")
        else:
            take = f"Neither trend nor video decided it alone: keep the top radar topic, bet on a strong hook and usefulness ({top})."

    # ---- X keyword table
    xk_p = day / "_xkw" / "keywords.json"
    xkw = json.loads(xk_p.read_text()) if xk_p.exists() else None
    xrank = {r["keyword"].lower(): r["rank"] for r in (xkw or {}).get("keywords", [])}

    # ---- B) ideas + B2) articles (agent-written, validated)
    ideas, errs = inp.get("ideas") or [], []
    allk = {k.lower() for k, _ in kws} | set(xrank)
    tnames = {t["name"] for t in topics} | {r["keyword"] for r in (xkw or {}).get("keywords", [])}
    for i, it in enumerate(ideas, 1):
        for f in ("title", "hook_en", "angle", "topic", "keywords", "format", "why", "visual", "visual_type"):
            if not it.get(f):
                errs.append(f"idea {i}: missing {f}")
        if it.get("visual_type") not in VISUALS:
            errs.append(f"idea {i}: visual_type must be one of {sorted(VISUALS)} (no text-only posts)")
        if not set(re.split(r"[ /+,]+", str(it.get("format", "")).lower())) & VISUALS:
            errs.append(f"idea {i}: format must include a visual ({sorted(VISUALS)}), got '{it.get('format')}'")
        if any(ch in str(it.get("hook_en", "")) + str(it.get("title", "")) for ch in BANNED_DASHES):
            errs.append(f"idea {i}: em/en dash")
        bad = [k for k in it.get("keywords", []) if k.lower() not in allk]
        if bad:
            errs.append(f"idea {i}: keywords not in trend list / X keyword table {bad}")
        hay = (str(it.get("hook_en", "")) + " " + str(it.get("angle", ""))).lower()
        miss = [k for k in it.get("keywords", []) if k.lower() not in hay]
        if miss:
            errs.append(f"idea {i}: keywords not used in hook/angle {miss}")
        if it.get("topic") and it["topic"] not in tnames:
            errs.append(f"idea {i}: topic '{it['topic']}' not in radar topics / X keywords")
        if re.match(r"\s*@", str(it.get("hook_en", ""))):
            errs.append(f"idea {i}: reads like a reply - ideas are standalone posts")
        xs = sorted(xrank[k.lower()] for k in it.get("keywords", []) if k.lower() in xrank)
        it["x_keywords"] = [k for k in it.get("keywords", []) if k.lower() in xrank]
        it["x_rank"] = xs[0] if xs else None
        it["source"] = "x-keywords" if xs else "watchlist-virals"
    if xkw and ideas:
        nx = sum(1 for it in ideas if it["x_rank"])
        if nx < math.ceil(0.6 * len(ideas)):
            errs.append(f"only {nx}/{len(ideas)} ideas use an X keyword-table keyword (need >= 60%)")
        top5 = {r["keyword"].lower() for r in xkw["keywords"][:5]}
        if not any(k.lower() in top5 for it in ideas for k in it.get("keywords", [])):
            errs.append("no idea uses any of the top-5 X keywords")
        ideas.sort(key=lambda it: (it["x_rank"] is None, it["x_rank"] or 99))
    if need_ideas and not (5 <= len(ideas) <= 8):
        errs.append(f"need 5-8 ideas in {inp_p} (have {len(ideas)})")
    arts = inp.get("articles") or []
    for i, ar in enumerate(arts, 1):
        for f in ("title", "thesis", "outline", "keywords", "visual", "why"):
            if not ar.get(f):
                errs.append(f"article {i}: missing {f}")
        if not (3 <= len(ar.get("outline") or []) <= 7):
            errs.append(f"article {i}: outline needs 3-7 points")
        if any(ch in str(ar.get("title", "")) + str(ar.get("thesis", "")) + " ".join(ar.get("outline") or []) for ch in BANNED_DASHES):
            errs.append(f"article {i}: em/en dash")
        bad = [k for k in ar.get("keywords", []) if k.lower() not in allk]
        if bad:
            errs.append(f"article {i}: keywords not in trend list / X keyword table {bad}")
        if xkw and not any(k.lower() in xrank for k in ar.get("keywords", [])):
            errs.append(f"article {i}: must use at least one X keyword-table keyword")
        ar["x_keywords"] = [k for k in ar.get("keywords", []) if k.lower() in xrank]
    if need_ideas and not (2 <= len(arts) <= 3):
        errs.append(f"need 2-3 articles in {inp_p} (have {len(arts)})")
    if errs:
        print("RADAR REJECTED:\n  " + "\n  ".join(errs), file=sys.stderr)
        sys.exit(3)

    d["lang"] = str(cfg.get("lang") or "en").lower()
    d["trend_radar"] = {
        "date": D, "title": "Trends and post ideas",
        "window": {"end": end.isoformat(), "label24": f"{s24:%d.%m %H:%M} - {end:%d.%m %H:%M} UTC",
                   "label48": f"{s48:%d.%m %H:%M} - {end:%d.%m %H:%M} UTC"},
        "corpus": {"posts": len(posts), "min_views": floor,
                   "lanes": {l: sum(1 for p in posts.values() if p["lane"] == l)
                             for l in ("watchlist", "outsider", "24h", "trend_input")}},
        "summary": {"top10_line": top10_line, "headline": headline, "takeaway": take, "stats": S},
        "topics": topics[:8], "ideas": ideas, "articles": arts, "why_hit": why,
        "labels": L,
        "x_keywords": ({k: xkw.get(k) for k in ("fetched_at", "window_start", "calls", "method", "missing", "sample",
                                                 "sample_size_per_call")} | {"keywords": xkw["keywords"][:20]}) if xkw else None,
        "legend": (f"Trend match 0-100% = 1 - prod(1 - w) over matched 24 h keywords that another author also used in the "
                   f"48 h window (w: rank 1-10 0.35, 11-25 0.22, 26-40 0.12, curated 0.20). Verdict: >= {TREND_CUT}% -> "
                   f"{L['trend']}; else video/image in the post data -> {L['visual']}; else >= 100K followers (outsiders without "
                   f"follower data: >= 500K views, estimate) -> {L['author']}; else {L['other']}. Missing data shows as "
                   f"'{L['no_data']}'. Heat = sum log10(views) of topic posts (24 h x1, 24-48 h x0.5), scaled to 100. "
                   f"Momentum = log-views last 24 h / previous 24 h. Trend-input-only accounts feed the corpus but are never "
                   f"shown as hits."),
    }
    save_data(d)
    print(f"trend_radar: topics={len(topics)} ideas={len(ideas)} articles={len(arts)} why_hit={len(why)} | {top10_line}")
    print(f"  {headline}")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "build":
        sys.exit(__doc__)
    build(sys.argv[2], need_ideas="--no-ideas-ok" not in sys.argv)
