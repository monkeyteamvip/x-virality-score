# X Virality Score: the free desk that tells beginners what to post

I used to open X every morning and still freeze.

I scrolled. I liked other people's posts. I still did not know what I should write today. The formats that worked last week already felt old. By the time I finished reading, the meta had moved again.

I did not need another content course. I needed a simple desk that shows me what is printing right now, and leaves me drafts I can edit in my own voice.

So I built **X Virality Score**: a free public experimental tool for creators. Handle: @thegreatest_sv

Repo: https://github.com/monkeyteamvip/x-virality-score

![](assets/article/x-virality-score-hero.png)

## The problem in plain words

I did not know what to post.

Not because I never tried. Because I was out of meta. I was guessing. Posts landed soft. Other accounts in my niche kept hitting formats I only noticed the day after.

What I wanted, every day, in simple language:

- see what already cleared a view floor
- keep the full text, not a vague summary
- get drafts I can tweak and ship
- peek at meta outside my usual list
- spend less morning time scrolling

Rough numbers from my own desk: about ~3 hours/day back. About ~$1k/mo I am not paying assistants to research and first-draft the same pile. I publish 1-2 posts/day.

This is experimental. No big promise. Just a tool that helps beginners follow virality without drowning.

![](assets/article/tasks-queue.png)

## What I built

**X Virality Score** is a free public experimental desk.

It is not an autoposter. It is not an engagement farm. Engagement helpers, if any, stay beta only. One line, then we move on.

You stay the publisher. The desk does the chores.

![](assets/article/pixel-office.png)

![](assets/article/coding-hud.png)

## How it works (simple steps)

### 1. Put your account list in config

Open config/watchlist.json and drop in the handles you want to learn from. Your niche. Your curriculum. Mine is about eighteen accounts. Yours can be totally different.

### 2. It reads original posts over a view floor

It looks at profiles, Posts only, originals, not replies. Default floor: 5k views. Stars at 10k. Timezone Europe/Moscow. Target: digest ready before noon.

### 3. It finds keywords and patterns

This is the part that made drafts start working.

The desk pulls recurring phrases, names, and structures from watchlist hits and outsiders. Cold opens. Numbered stacks. Named tools. Soft CTAs. Real patterns, not vibes.

![](assets/article/keywords-terminal.png)

### 4. It writes drafts from those keywords

Not "rewrite this post." Write from the pattern brief:

keywords → pattern brief → English draft + short video tip

You keep the energy that already traveled. You do not clone the original.

![](assets/article/draft-from-keywords.png)

### 5. It also checks ~20 outside posts for today's meta

Your watchlist is school. Outsiders are the weather.

About 20 AI posts from the last ~48 hours, beyond the accounts you already track. Same keyword pass. Wider meta. No fossil hits from last month.

![](assets/article/meta-outsiders.png)

## Who it is for

Beginner bloggers and creators who want to follow virality without drowning.

If you:

- post on X but feel late to every trend
- waste mornings scrolling and still blank out
- want a small daily stack of drafts, not a 40-tab rabbit hole

this desk is for you.

Power users can fork the watchlist for any niche. The beginner case is the point.

## What changes for you

Before: scroll until your eyes hurt, guess the meta, stare at an empty draft box, ship 0-1 panicked posts, maybe pay someone to research.

After: the desk scouts before noon, you see watchlist hits plus 48h outsiders, you get a draft pile from keyword patterns, you ship a steady 1-2 posts/day, and you get ~3h/day back (about ~$1k/mo not spent on assistants).

You still choose the voice. You still hit publish. The bots refuse to scroll for free inside your head.

![](assets/article/digest-report.png)

## Roles on the desk (plain words)

Think of it like a tiny office:

- Scout reads the accounts and finds posts over the view floor
- Draft turns mined keywords into English drafts you can edit
- Board shows X Score, Day Target, and per-hit chips so you see DONE / NOT DONE at a glance
- You publish

That is the whole loop.

![](assets/article/x-virality-score-board.png)

Per-hit chips are what I actually scan while editing:

![](assets/article/x-virality-score-hit-target.png)

## One receipt from my own account

I am not inventing a follower chart. Here is a post that already printed:

Claude bug-hunter desk · Part 2 (https://x.com/thegreatest_sv/status/2071564762027114875): about 2.08M views.

That is the energy the desk chases: formats that already work, rewritten in my lane, shipped 1-2 times a day.

![](assets/article/claude-bughunter-2m-views.png)

## Do this right now

1. Open https://github.com/monkeyteamvip/x-virality-score
2. Copy the example watchlist and put your accounts in config/watchlist.json
3. Point a Grok Bot agent at AGENTS.md (or add the template: https://x.ai/bot/qG9mJ4EM-96hA3A1UNw4E)
4. Keep a read-only X session on the box browser
5. Ask for a digest tomorrow before noon
6. Open the board. Check X Score and Day Target
7. Pick one draft. Edit it in your voice. Ship it
8. Ship a second one if it still feels warm

![](assets/article/terminal-pack.png)

## Live board + links

Public free experimental board (updates when digests land):

https://monkeyteamvip.github.io/kiosa-board/

GitHub: https://github.com/monkeyteamvip/x-virality-score

Bot Marketplace: Add the bot here:
https://x.ai/bot/qG9mJ4EM-96hA3A1UNw4E

X Virality Score · @thegreatest_sv

Privacy (short): experimental personal tooling. No personal data collection from visitors. No tracking cookies. Read-only X scrape via the operator session, not visitor accounts. Not affiliated with X/Twitter Corp. Third-party posts belong to their authors. No warranty.

I started guessing. I stopped.

The free desk shows beginners what to post. @thegreatest_sv is the publisher. You keep the byline.
