#!/usr/bin/env python3
"""Offline sample day. No network, no X account, no personal config.

Proves a fresh tree can run pipeline/run_day.sh and emit an English ping
plus the static board (index.html + data.json).

  python3 scripts/smoke_day.py
  bash scripts/smoke_day.sh
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIX = REPO / "fixtures" / "sample-day"
DAY = "2026-10-26"
CYR = re.compile("[\u0400-\u04FF]")
# Russian stays available when config lang is "ru". These files are the only
# places that ship those strings. board/index.html may match the ru verdict
# words so badges still color when lang is ru.
RU_FILES = {
    "pipeline/common.py",
    "pipeline/ping.py",
    "pipeline/radar.py",
    "templates/DIGEST_TEMPLATE.md",
}
SKIP_DIRS = {".git", ".smoke-preview", "__pycache__", "node_modules"}


def run(cmd: list[str], env: dict) -> None:
    proc = subprocess.run(cmd, cwd=REPO, env=env, text=True, capture_output=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        sys.exit(proc.returncode or 1)
    if proc.stdout.strip():
        print(proc.stdout.strip())


def make_draft(text: str, keywords: list[str]) -> dict:
    cands = [k for k in keywords if k.lower() in text.lower() and len(k.split()) <= 4]
    kw = cands[0] if cands else (keywords[0] if keywords else "note")
    draft = (
        f"Keep this angle if you post about {kw}. "
        "Someone already proved the format in public: one habit, one failure mode, no extra claims. "
        "Tell that same story with your own setup and leave every figure as printed."
    )
    return {"draft_en": draft, "keywords_used": [kw]}


def scan_english() -> None:
    bad = []
    for path in REPO.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in {".md", ".py", ".html", ".json", ".sh", ".yml", ".yaml", ".txt"}:
            continue
        rel = path.relative_to(REPO).as_posix()
        if rel in RU_FILES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if rel == "board/index.html":
            text = "\n".join(line for line in text.splitlines() if "vbClass" not in line)
        if CYR.search(text):
            bad.append(rel)
    if bad:
        sys.exit("Cyrillic in user-facing files (Russian belongs behind lang=ru only):\n  " + "\n  ".join(bad))


def assert_neutral_defaults() -> None:
    example = json.loads((REPO / "config" / "watchlist.example.json").read_text())
    if example.get("lang") != "en":
        sys.exit("config/watchlist.example.json lang must default to en")
    if example.get("timezone") != "UTC":
        sys.exit("config/watchlist.example.json timezone must default to UTC")
    accounts = example.get("accounts") or []
    if "example_account" not in accounts or "your_handle" in json.dumps(accounts):
        sys.exit("watchlist example must keep placeholder accounts")
    blob = ""
    for path in (REPO / "config").rglob("*.json"):
        blob += path.read_text(encoding="utf-8")
    blob += (REPO / "board" / "data.example.json").read_text(encoding="utf-8")
    blob += (REPO / "board" / "index.html").read_text(encoding="utf-8")
    for needle in ("thegreatest_sv", "kiosa", "monkeyteamvip"):
        if needle.lower() in blob.lower():
            sys.exit(f"default config/board still contains {needle}")
    html = (REPO / "board" / "index.html").read_text(encoding="utf-8")
    for label in ("X Score", "Day Target", "Outsiders · last 48h"):
        if label not in html:
            sys.exit(f"board HTML missing English label: {label}")


def main() -> None:
    assert_neutral_defaults()
    scan_english()
    work = Path(tempfile.mkdtemp(prefix="xvs-smoke-"))
    try:
        digest = work / "digests"
        data_path = work / "data.json"
        shutil.copy(FIX / "data.json", data_path)
        prior = digest / "2026-10-20" / "_parts"
        prior.mkdir(parents=True)
        shutil.copy(FIX / "prior_trend_keywords.json", prior / "trend_keywords.json")
        env = os.environ.copy()
        env["XVS_DIGEST_ROOT"] = str(digest)
        env["XVS_DATA"] = str(data_path)
        env["XVS_WATCHLIST"] = str(FIX / "watchlist.json")
        run(["bash", "pipeline/run_day.sh", "prepare", DAY], env)

        req_path = digest / DAY / "_xkw" / "request.json"
        req = json.loads(req_path.read_text())
        expected = {
            "claude_code__24h.json",
            "claude_code__prev24h.json",
            "prompt_injection__24h.json",
            "prompt_injection__prev24h.json",
        }
        got = {c["file"] for c in req["calls"]}
        if got != expected:
            sys.exit(f"sample x keyword files {sorted(got)} != {sorted(expected)}")
        for name in expected:
            shutil.copy(FIX / "xkw" / name, digest / DAY / "_xkw" / name)

        trend = json.loads((digest / DAY / "_parts" / "trend_keywords.json").read_text())
        keywords = [r["keyword"] for r in trend.get("keywords") or []]
        if not keywords:
            sys.exit("sample day produced no trend keywords")
        originals = json.loads((digest / DAY / "_parts" / "originals.json").read_text())
        drafts = {pid: make_draft(row["text"], keywords) for pid, row in originals.items()}
        if len(drafts) < 1:
            sys.exit("sample day produced no TOP-10 posts")
        parts = digest / DAY / "_parts"
        (parts / "drafts_v4.json").write_text(json.dumps(drafts, indent=2) + "\n")
        shutil.copy(FIX / "radar_inputs.json", parts / "radar_inputs.json")
        exp = digest / DAY / "_exp"
        exp.mkdir(parents=True, exist_ok=True)
        shutil.copy(FIX / "timeline.json", exp / "timeline.json")

        run(["bash", "pipeline/run_day.sh", DAY], env)

        ping = (digest / DAY / "PING.txt").read_text(encoding="utf-8")
        data = json.loads(data_path.read_text())
        problems = []
        if CYR.search(ping):
            problems.append("ping contains Cyrillic while lang is en")
        for bit in (
            "X digest 26.10:",
            "hits ≥5k",
            "self-quotes:",
            "outsiders.",
            "X keywords 24h (sample):",
            "TOP-10:",
            "Experiment @your_handle",
            "Board: https://your-github-user.github.io/x-virality-board/",
        ):
            if bit not in ping:
                problems.append(f"ping missing {bit!r}")
        handles = [str(h.get("handle") or "") for h in data.get("hits") or []]
        if any("aggregator" in h.lower() for h in handles):
            problems.append("trend_input_only account still listed as a hit")
        moved = data.get("trend_input_only_posts") or []
        if not any("aggregator" in str(p.get("handle") or "").lower() for p in moved):
            problems.append("aggregator post was not moved to trend_input_only_posts")
        line = ((data.get("trend_radar") or {}).get("summary") or {}).get("top10_line") or ""
        if not line.startswith("TOP-10:"):
            problems.append(f"top10 line is not English: {line!r}")
        if CYR.search(line):
            problems.append("top10 line contains Cyrillic")
        drafted = [h for h in (data.get("hits") or []) + (data.get("virals") or []) if h.get("draft_en")]
        if len(drafted) < 1:
            problems.append("no English drafts applied to the board")
        if not (data.get("experiment") or {}).get("verdict"):
            problems.append("experiment verdict missing")
        if problems:
            sys.stderr.write(ping + "\n")
            sys.exit("sample day failed:\n  " + "\n  ".join(problems))

        preview = REPO / "board" / ".smoke-preview"
        if preview.exists():
            shutil.rmtree(preview)
        preview.mkdir(parents=True)
        shutil.copy(REPO / "board" / "index.html", preview / "index.html")
        shutil.copy(data_path, preview / "data.json")
        print("--- PING (English) ---")
        print(ping.rstrip())
        print(f"Board preview: {preview}/  (index.html + data.json)")
        print("OK sample day")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
