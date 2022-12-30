#!/usr/bin/env python3
"""
Telegram Bot Auto-Discovery Crawler
Continuously discovers, validates, and categorizes new Telegram bots
from multiple public repositories, Telegram channels, and directories.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from typing import Dict, List, Set

from check_bots import BotChecker

DATA_FILE = "data/bots.json"
README_FILE = "README.md"
DISCOVERY_REPORT = "DISCOVERED_BOTS.md"

# Reputable public sources that index Telegram bots
SOURCES = [
    "https://t.me/s/botlist",
    "https://raw.githubusercontent.com/danyspin97/TelegramBotsList/master/README.md",
    "https://raw.githubusercontent.com/TayaSoboleva/awesome_telegram/master/README.md",
    "https://raw.githubusercontent.com/ebertti/awesome-telegram/master/README.md",
    "https://raw.githubusercontent.com/flutegram/awesome-telegram/main/README.md",
]

CATEGORY_KEYWORDS = {
    "ai-assistants": [r"\bai\b", r"\bgpt\b", "chatgpt", "claude", "gemini", "whisper", "transcribe", "voice to text", "dall-e", "midjourney", "diffusion", "artificial intelligence"],
    "file-converters": ["convert", "pdf", "docx", "epub", "watermark", "compress", "resize image", "optimize"],
    "media-downloaders": ["download", "downloader", "youtube", "tiktok", "instagram", "reels", "twitter", "pinterest", "reddit", "save video", "uploader"],
    "music-audio": ["music", "song", "spotify", "soundcloud", "mp3", "flac", "deezer", "audio", "lyrics", "shazam", "radio", "spleeter"],
    "movies-tv": ["movie", "cinema", "imdb", "series", "episodes", "film", "stream"],
    "cloud-torrent": ["torrent", "magnet", "seedr", "cloud", "uploader", "direct link", "drive", "disk"],
    "privacy-security": ["antivirus", "virus", "malware", "temp mail", "disposable", "fakemail", "security", "truecaller", "spam", "blocker", "nsfw"],
    "group-moderation": ["admin", "moderation", "anti-spam", "anti-flood", "captcha", "ban", "mute", "welcome", "roles", "groups", "filter", "mention"],
    "developers-devops": ["github", "gitlab", "json", "code", "compiler", "regex", r"\bapi\b", "whois", "dns", "devops", "docker"],
    "productivity-utilities": ["reminder", "calendar", "todo", "task", "qr", "shorten", "calculator", "notes", "rss", "feed", "flight", "aviation", "timer", "clock", "price"],
    "search-reference": ["wikipedia", "wiki", "dictionary", "search", "gif", "tenor", "thesaurus", "news", "map", "pronunciation", "emoji"],
    "stickers-themes": ["sticker", "theme", "latex", "font", "graphic", "logo"],
    "telegram-utils": ["chat id", "user info", "analytics", "tgstat", "channel", "members"],
    "crypto-finance": ["crypto", "bitcoin", "ethereum", "wallet", "price", "dex", "token", "trading"],
    "sports-alerts": ["sport", "football", "soccer", "live score", "fixture", "match"]
}

def load_existing_handles() -> Set[str]:
    if not os.path.exists(DATA_FILE):
        return set()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    handles = set()
    for cat in data.get("categories", []):
        for b in cat.get("bots", []):
            handles.add(b["handle"].lower().lstrip("@"))
    return handles

def scrape_sources() -> Set[str]:
    discovered = set()
    print("🌐 Scraping public bot sources for new handles...")
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                
                # Match @handle or t.me/handle
                mentions = re.findall(r"@([A-Za-z0-9_]{3,32}bot)\b", html, re.IGNORECASE)
                links = re.findall(r"t\.me/([A-Za-z0-9_]{3,32}bot)\b", html, re.IGNORECASE)
                
                found_here = set([h.lower() for h in mentions + links])
                discovered.update(found_here)
                print(f"  ✓ {url[:55]}... -> found {len(found_here)} bot handles")
        except Exception as e:
            print(f"  ✗ {url[:55]}... -> Error: {e}")

    return discovered

def categorize_bot(title: str, description: str) -> str:
    text = f"{title} {description}".lower()
    for cat_id, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw.startswith(r"\b") or kw.endswith(r"\b"):
                if re.search(kw, text):
                    return cat_id
            elif kw in text:
                return cat_id
    return "productivity-utilities"

def merge_new_bots(new_bots: List[Dict]):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cat_map = {c["category_id"]: c for c in data["categories"]}
    added_count = 0

    for bot in new_bots:
        cat_id = bot["category_id"]
        if cat_id in cat_map:
            # Check if handle already exists
            existing = {b["handle"].lower() for b in cat_map[cat_id]["bots"]}
            if bot["handle"].lower() not in existing:
                cat_map[cat_id]["bots"].append({
                    "name": bot["name"],
                    "handle": bot["handle"],
                    "desc": bot["desc"],
                    "tags": bot.get("tags", [cat_id.split("-")[0].capitalize()])
                })
                added_count += 1

    total = sum(len(c["bots"]) for c in data["categories"])
    data["metadata"]["total_bots"] = total
    data["metadata"]["updated_at"] = "Auto-Discovered & Verified"

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✨ Successfully added {added_count} new bots! New catalog total: {total} bots.")
    
    # Rebuild README.md
    from merge_and_build import build_readme
    build_readme(total)

def main():
    parser = argparse.ArgumentParser(description="Auto-discover new active Telegram bots.")
    parser.add_argument("--limit", type=int, default=15, help="Maximum new verified bots to add per run")
    parser.add_argument("--auto-merge", action="store_true", help="Automatically merge new bots into data/bots.json and README.md")
    args = parser.parse_args()

    existing = load_existing_handles()
    print(f"📖 Loaded {len(existing)} existing bots from catalog.")

    raw_discovered = scrape_sources()
    # Filter out already known bots
    candidates = [h for h in raw_discovered if h.lower() not in existing and not h.lower().startswith("botfather")]

    print(f"\n🔍 Found {len(candidates)} new candidate handles not in the catalog.")
    if not candidates:
        print("No new candidates found.")
        sys.exit(0)

    # Validate candidates using BotChecker
    print(f"🧪 Testing candidates for liveness (checking first {min(len(candidates), 60)} candidates)...")
    sample_to_test = candidates[:60]
    
    checker = BotChecker(timeout=8, max_workers=15)
    results = checker.check_all(sample_to_test)

    alive = [r for r in results if r["status"] == "alive"]
    print(f"\n🎯 Verified Active Bots: {len(alive)}")

    new_bot_entries = []
    for bot in alive[:args.limit]:
        title = bot.get("title") or bot["handle"]
        # Clean title
        clean_title = re.sub(r"[^\w\s-]", "", title).strip() or bot["handle"]
        desc = bot.get("description") or f"Useful Telegram bot for daily messaging and tasks."
        # Keep description clean and concise
        if len(desc) > 160:
            desc = desc[:157] + "..."
        if not desc or desc.lower() == "none":
            desc = f"Active Telegram bot for {clean_title}."

        cat_id = categorize_bot(clean_title, desc)
        
        new_bot_entries.append({
            "name": clean_title,
            "handle": bot["handle"],
            "desc": desc,
            "category_id": cat_id,
            "tags": [cat_id.split("-")[0].capitalize(), "Verified"]
        })

    # Output report
    report_lines = [
        "# 🌟 Newly Discovered Telegram Bots",
        "",
        f"*Discovered {len(new_bot_entries)} verified active bots.*",
        "",
        "| Bot Name | Handle | Category | Description |",
        "| --- | --- | --- | --- |"
    ]
    for b in new_bot_entries:
        report_lines.append(f"| **{b['name']}** | [@{b['handle']}](https://t.me/{b['handle']}) | `{b['category_id']}` | {b['desc']} |")

    with open(DISCOVERY_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")
    print(f"📄 Candidate report saved to {DISCOVERY_REPORT}.")

    if args.auto_merge and new_bot_entries:
        merge_new_bots(new_bot_entries)

if __name__ == "__main__":
    main()
