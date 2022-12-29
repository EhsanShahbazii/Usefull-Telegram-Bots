# 🤝 Contributing to Useful Telegram Bots

Thank you for your interest in contributing to **Useful Telegram Bots**! We welcome community recommendations to keep this directory high-quality, up-to-date, and useful for everyone.

---

## 📌 Submission Guidelines

Before proposing a new bot, please ensure it meets the following standards:

1. **Active & Operational**: The bot must be online and responsive. Its `t.me/<handle>` link must be active with a working `Start Bot` button.
2. **High Utility**: The bot should solve a real need (e.g., productivity, AI, conversion, moderation, media retrieval).
3. **No Malicious Behavior**: Bots promoting scams, malware, abusive spam, or deceptive paywalls will be rejected immediately.
4. **Accessible**: The bot must offer free features or a generous free tier without requiring mandatory invasive payments.

---

## 🛠️ How to Add a Bot

1. **Fork** the repository and clone your fork locally.
2. Open `scripts/merge_and_build.py` and find the relevant category in `CATALOG`.
3. Add your bot entry following this structure:
   ```python
   {
       "name": "Bot Display Name",
       "handle": "username_without_at_bot",
       "desc": "A concise 1-2 sentence description explaining what the bot does.",
       "tags": ["Tag1", "Tag2"]
   }
   ```
4. Regenerate `data/bots.json` and `README.md`:
   ```bash
   python3 scripts/merge_and_build.py
   ```
5. Run the liveness checker to ensure your bot passes validation:
   ```bash
   python3 scripts/check_bots.py --handles your_bot_handle
   ```
6. Commit your changes and open a **Pull Request** with a brief summary of the bot.

---

## 🐛 Reporting Dead or Inactive Bots

If you notice a bot has ceased functioning or was deleted:
- Open a GitHub Issue using the **Report Broken Bot** template.
- Or submit a PR updating `scripts/merge_and_build.py` to prune the dead handle.

---

## 🧪 Testing Locally

To run the automated verification tool across the entire catalog:
```bash
python3 scripts/check_bots.py --json data/bots.json --report BOT_HEALTH.md
```

Thank you for making this community catalog awesome! ❤️
