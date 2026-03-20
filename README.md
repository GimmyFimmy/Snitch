![banner](docs/banner.png)

<div align="center">

[![Documentation](https://img.shields.io/badge/docs-online-4ade80?style=flat-square)](https://GimmyFimmy.github.io/Snitch/)
[![Python](https://img.shields.io/badge/language-Python-60a5fa?style=flat-square)]()
[![Flask](https://img.shields.io/badge/server-Flask-f87171?style=flat-square)]()
[![Discord](https://img.shields.io/badge/bot-nextcord-a87ef5?style=flat-square)]()

Snitch forwards GitHub webhook events to Discord channels as rich embeds. It registers a webhook on your repository at startup, tunnels incoming requests via smee.io, and removes the webhook automatically on exit.

Instead of manually setting up webhooks, ngrok tunnels, and Discord bots separately, you drop two config files and call `Snitch()`. Everything else is handled for you.

```
GitHub repo ──► smee.io tunnel ──► Flask server ──► Discord bot ──► your channels
```

---

## Example

`main.py`
```python
from snitch import Snitch

Snitch()
```

`snitch/config/events.json`
```json
{
    "color": { "r": 121, "g": 65, "b": 231 },

    "push": {
        "channel_id": 123456789012345678,
        "title": "↗ Push from {data[pusher][name]}",
        "desc": "`Commit: {data[head_commit][message]}`\n`Forced: {data[forced]}`"
    },
    "issues": {
        "channel_id": 123456789012345678,
        "title": "⚠ {data[issue][title]} was *{data[action]}* by {data[issue][user][login]}",
        "desc": "`Id: {data[issue][id]}`"
    }
}
```

Add any [GitHub event name](https://docs.github.com/en/webhooks/webhook-events-and-payloads) as a key. Use `{data[...]}` to reference fields from the payload. Events without a matching key are silently ignored.

For the full API reference, configuration options, and more examples, see the **[documentation](https://GimmyFimmy.github.io/Snitch/)**.

---

## Requirements

- Python `3.10+`
- Node.js (used internally for `smee-client`)
- Windows `10/11`

---

## Project structure

```
snitch/
├── config/
│   ├── tokens.env          ← secrets, never commit
│   ├── events.json         ← embed templates + channel IDs
│   └── webhooks.json       ← GitHub API config (auto-managed)
├── api/
│   ├── tunnel.py           ← smee.io tunnel
│   ├── webhook.py          ← GitHub webhook lifecycle
│   ├── client.py           ← Discord bot + embed builder
│   ├── server.py           ← Flask server, POST
│   └── utils/
│       ├── __env.py
│       ├── __json.py
│       ├── __logger.py
│       ├── __requests.py
│       └── __thread.py
└── __init__.py             ← Snitch() entrypoint
```

``Python 3.10`` ``Windows 10/11``

## Contributing

Contributions are welcome. If you find a bug, have a feature idea, or want to improve the docs, feel free to open an issue or a pull request.

A few things to keep in mind before submitting:

- **Keep it small.** Snitch is intentionally minimal. New features should solve a clear problem that can't already be handled by editing the config.

- **Match the style.** Use the `__` prefix for private methods and attributes, keep utilities in `snitch/api/utils/`, and follow the existing class-per-responsibility pattern.

- **One thing per PR.** Focused pull requests are easier to review and faster to merge.

If you're unsure whether an idea fits, open an issue first so we can discuss it before you write any code.
