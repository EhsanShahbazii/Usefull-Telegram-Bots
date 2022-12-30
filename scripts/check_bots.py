#!/usr/bin/env python3
"""
Telegram Bot Health & Liveness Verifier
Parses Telegram bot handles from README.md or data/bots.json,
verifies their existence and bot status via Telegram web previews,
and outputs detailed health metrics and reports.
"""

import argparse
import concurrent.futures
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from typing import Dict, List, Optional, Tuple

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

class BotChecker:
    def __init__(self, timeout: int = 8, max_workers: int = 15):
        self.timeout = timeout
        self.max_workers = max_workers

    def check_handle(self, handle: str) -> Dict:
        handle = handle.strip().lstrip("@")
        url = f"https://t.me/{handle}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        
        result = {
            "handle": handle,
            "url": url,
            "exists": False,
            "is_bot": False,
            "status": "dead",
            "title": "",
            "description": "",
            "error": None,
        }

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                html = resp.read().decode("utf-8", errors="ignore")

                # Check if page exists: either full preview or contact page with resolve link
                has_full_preview = '<div class="tgme_page_title"' in html
                page_title_match = re.search(r"<title>(.*?)</title>", html)
                page_title_text = page_title_match.group(1) if page_title_match else ""
                has_contact_page = f"Contact @{handle}" in page_title_text or "Telegram: Contact @" in page_title_text
                has_resolve_link = f"tg://resolve?domain={handle}" in html or "tg://resolve?domain=" in html

                if not (has_full_preview or (has_contact_page and has_resolve_link)):
                    result["status"] = "dead"
                    return result

                result["exists"] = True

                # Extract display title
                title_match = re.search(r'<div class="tgme_page_title"[^>]*>(.*?)</div>', html, re.DOTALL)
                if title_match:
                    raw_title = re.sub(r"<[^<]+?>", "", title_match.group(1)).strip()
                    result["title"] = raw_title

                # Extract description
                desc_match = re.search(r'<div class="tgme_page_description"[^>]*>(.*?)</div>', html, re.DOTALL)
                if desc_match:
                    raw_desc = re.sub(r"<[^<]+?>", "", desc_match.group(1)).strip()
                    result["description"] = raw_desc
                else:
                    og_desc = re.search(r'<meta property="og:description" content="([^"]+)">', html)
                    if og_desc:
                        import html as html_module
                        result["description"] = html_module.unescape(og_desc.group(1).strip())

                # Check action button
                action_match = re.search(r'<div class="tgme_page_action"[^>]*>(.*?)</div>', html, re.DOTALL)
                action_html = action_match.group(1) if action_match else ""

                if "Start Bot" in action_html or ("tg://resolve?domain=" in action_html and ("bot" in handle.lower() or "Start" in action_html)):
                    result["is_bot"] = True
                    result["status"] = "alive"
                elif "View in Telegram" in action_html or "View Channel" in action_html or "Join Channel" in action_html:
                    result["is_bot"] = False
                    result["status"] = "channel_or_group"
                else:
                    result["is_bot"] = False
                    result["status"] = "user_or_other"

        except Exception as e:
            result["error"] = str(e)
            result["status"] = "error"

        return result

    def check_all(self, handles: List[str]) -> List[Dict]:
        handles = list(dict.fromkeys(handles))  # Preserve unique handles
        results = []
        total = len(handles)

        print(f"🚀 Starting verification of {total} Telegram handles with {self.max_workers} threads...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_handle = {executor.submit(self.check_handle, h): h for h in handles}
            completed = 0
            for future in concurrent.futures.as_completed(future_to_handle):
                completed += 1
                data = future.result()
                results.append(data)
                status_icon = "🟢" if data["status"] == "alive" else ("⚠️" if data["status"] != "dead" else "🔴")
                print(f"[{completed}/{total}] {status_icon} @{data['handle']:<25} -> {data['status']}")

        return results


def extract_handles_from_readme(readme_path: str) -> List[str]:
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    handles = re.findall(r"https://t\.me/([A-Za-z0-9_]+)", content)
    ignored = {"BotFather", "s", "joinchat", "share", "addstickers"}
    return [h for h in handles if h not in ignored]


def extract_handles_from_json(json_path: str) -> List[str]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    handles = []
    if isinstance(data, list):
        for b in data:
            if "handle" in b:
                handles.append(b["handle"])
    elif isinstance(data, dict):
        if "bots" in data and isinstance(data["bots"], list):
            for b in data["bots"]:
                if "handle" in b:
                    handles.append(b["handle"])
        if "categories" in data and isinstance(data["categories"], list):
            for cat in data["categories"]:
                for b in cat.get("bots", []):
                    if "handle" in b:
                        handles.append(b["handle"])
    return handles


def generate_markdown_report(results: List[Dict], output_file: str):
    alive = [r for r in results if r["status"] == "alive"]
    other = [r for r in results if r["status"] in ("channel_or_group", "user_or_other")]
    dead = [r for r in results if r["status"] in ("dead", "error")]
    total = len(results)

    lines = [
        "# 📊 Telegram Bots Health Report",
        "",
        f"*Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}*",
        "",
        "## 📈 Summary",
        f"- **Total Checked**: {total}",
        f"- **🟢 Active Bots**: {len(alive)} ({len(alive)/total*100:.1f}%)" if total else "",
        f"- **⚠️ Channels/Users**: {len(other)} ({len(other)/total*100:.1f}%)" if total else "",
        f"- **🔴 Dead / Unavailable**: {len(dead)} ({len(dead)/total*100:.1f}%)" if total else "",
        "",
    ]

    if dead:
        lines.extend([
            "## 🔴 Inactive or Dead Handles (Need Attention/Pruning)",
            "| Handle | Telegram Link | Issue |",
            "| --- | --- | --- |",
        ])
        for r in dead:
            err = r.get("error") or "Page not found / account deleted"
            lines.append(f"| `@{r['handle']}` | [Open](https://t.me/{r['handle']}) | {err} |")
        lines.append("")

    if other:
        lines.extend([
            "## ⚠️ Handles Changed to Channel/User",
            "| Handle | Title | Status |",
            "| --- | --- | --- |",
        ])
        for r in other:
            title = r.get("title") or "N/A"
            lines.append(f"| `@{r['handle']}` | {title} | {r['status']} |")
        lines.append("")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n✅ Health report generated at: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Verify Telegram bots status and liveness.")
    parser.add_argument("--readme", default="README.md", help="Path to README.md file")
    parser.add_argument("--json", default=None, help="Path to JSON data file")
    parser.add_argument("--handles", nargs="*", help="Direct list of handles to check")
    parser.add_argument("--report", default="BOT_HEALTH.md", help="Output health report markdown file")
    parser.add_argument("--workers", type=int, default=15, help="Number of concurrent workers")
    parser.add_argument("--timeout", type=int, default=8, help="Request timeout in seconds")

    args = parser.parse_args()

    handles = []
    if args.handles:
        handles = args.handles
    elif args.json and os.path.exists(args.json):
        handles = extract_handles_from_json(args.json)
    elif os.path.exists(args.readme):
        handles = extract_handles_from_readme(args.readme)
    else:
        print("Error: No valid source of handles provided.")
        sys.exit(1)

    if not handles:
        print("No handles found to verify.")
        sys.exit(0)

    checker = BotChecker(timeout=args.timeout, max_workers=args.workers)
    results = checker.check_all(handles)

    alive = [r for r in results if r["status"] == "alive"]
    dead = [r for r in results if r["status"] in ("dead", "error")]
    other = [r for r in results if r["status"] in ("channel_or_group", "user_or_other")]

    print("\n" + "=" * 50)
    print(f"🎯 Health Check Complete: {len(results)} total")
    print(f"🟢 Active Bots: {len(alive)}")
    print(f"⚠️  Changed / Non-Bot: {len(other)}")
    print(f"🔴 Dead / Inactive: {len(dead)}")
    print("=" * 50)

    if args.report:
        generate_markdown_report(results, args.report)


if __name__ == "__main__":
    main()
