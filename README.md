# ![Snitch](docs/banner.png)

> Forward GitHub events to Discord channels — zero config beyond tokens and a JSON file.

---

## How it works

```
GitHub repo → smee.io tunnel → Flask server → Discord bot → your channels
```

Snitch automatically creates a GitHub webhook for your repository on startup and removes it on exit. Events are forwarded as Discord embeds to whichever channels you configure in `events.json`.

---

## Requirements

- Python `3.10+`
- Node.js (used internally for `smee-client`)
- Windows 10/11

---

## Installation

```bash
# 1. Enter the repository
cd /path/to/snitch

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuration

All config lives in `snitch/config/`.

### 1. `tokens.env` — your secrets

```env
GITHUB_TOKEN=your_github_personal_access_token
BOT_TOKEN=your_discord_bot_token
```

> How to create a Discord bot and get a token: [discord.py docs](https://discordpy.readthedocs.io/en/stable/discord.html)

> **Never commit this file.** Add `tokens.env` to your `.gitignore`.

### 2. `events.json` — event templates and channel routing

Each event key must match a [GitHub webhook event name](https://docs.github.com/en/webhooks/webhook-events-and-payloads) exactly. Set `channel_id` to the Discord channel where that event should be posted. The `color` block controls the embed accent color across all events.

```json
{
    "color": {
        "r": 255,
        "g": 255,
        "b": 255
    },
    "push": {
        "channel_id": 123456789,
        "title": "↗ Push from {data[pusher][name]}",
        "desc": "`Commit Messages: {data[head_commit][message]}`\n`Forced: {data[forced]}`"
    },
    "pull_request": {
        "channel_id": 123456789,
        "title": "⤵ {data[pull_request][title]} was *{data[action]}* by {data[sender][login]}",
        "desc": "`Number: {data[number]}`"
    },
    "release": {
        "channel_id": 123456789,
        "title": "⬇ {data[release][name]} was *{data[action]}* by {data[release][author][login]}",
        "desc": "`Pre Release: {data[release][prerelease]}`\n`Id: {data[release][id]}`"
    },
    "issues": {
        "channel_id": 123456789,
        "title": "⚠ {data[issue][title]} was *{data[action]}* by {data[issue][user][login]}",
        "desc": "`Id: {data[issue][id]}`"
    }
}
```

Use `{data[...]}` to reference any field from the GitHub webhook payload. Use `\n` for line breaks in `desc`. You can add or remove events freely — any key not in this file is silently ignored.

---

## Usage

```python
from snitch import Snitch

Snitch()
```

That's it. `Snitch.__init__` reads tokens from `tokens.env`, spins up the smee.io tunnel, registers the GitHub webhook, starts the Discord bot, and runs the Flask server — all in the right order, with cleanup on exit.

---

## Project structure

```
snitch/
├── config/
│   ├── tokens.env          # GitHub + Discord tokens (never commit this)
│   ├── events.json         # Event templates, channel IDs, embed color
│   └── webhooks.json       # Webhook URL + payload config (auto-managed)
├── api/
│   ├── tunnel.py           # Creates smee.io tunnel, exposes payload URL
│   ├── webhook.py          # Registers and removes GitHub webhook
│   ├── client.py           # Discord bot, embed builder, message sender
│   ├── server.py           # Flask server, routes POST /
│   └── utils/
│       ├── __env.py        # Reads tokens from tokens.env
│       ├── __json.py       # JSON config reader + Flask response helper
│       ├── __logger.py     # Colored terminal logging (log_ok, log_err)
│       ├── __requests.py   # HTTP helpers (POST, DELETE, redirect)
│       └── __thread.py     # Thread + coroutine helpers
└── __init__.py             # Snitch() entrypoint — orchestrates everything
```

---

## Contribution

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.