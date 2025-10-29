<div><img src="/docs/banner.png" width=100% height=100%></div>

##

<div align="center">
Application to send GitHub events in a specific Discord channels.
</div>

## Getting started

### Software requirements

``Python 3.10`` or higher

##

### Installation (Via Terminal)

> [!TIP]
> We recommend downloading the latest release to avoid bugs.

1. Open the repository:
   ```commandline
   cd /path/to/repository
   ```
2. Create a new virtual environment:
   ```commandline
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```commandline
   source .venv/bin/activate
   ```
4. Update **pip**:
   ```commandline
   pip install --upgrade pip
   ```
5. Download packages:
   ```commandline
   pip install -r requirements.txt
   ```
   
##

### Creating Discord Bot

Information about how to create bot and get token can be found [here](https://discordpy.readthedocs.io/en/stable/discord.html).

##

### Usage

> [!CAUTION]
> This program is for personal use only. Do not share your bot tokens or text channel IDs with anyone.

First, we import **snitch** application. After that we call **run** method with **properties**.

> [!NOTE]
> Only **BOT_TOKEN** is required in **properties**, You can choose the channel to which event(s) will be sent or even ignore some type of event(s), according to your preference.

```python
from snitch import *

Snitch.run(properties={
    "BOT_TOKEN": "YOUR TOKEN HERE (REQUIRED)",
    "PUSH_CHANNEL_ID": "YOUR CHANNEL ID HERE",
    "PULL_REQUEST_CHANNEL_ID": "YOUR CHANNEL ID HERE",
    "RELEASE_CHANNEL_ID": "YOUR CHANNEL ID HERE",
    "ISSUES_CHANNEL_ID": "YOUR CHANNEL ID HERE",
})
```

##

### Creating GitHub webhook

Information about how to create repository webhook can be found [here](https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks).

> [!NOTE]
> After running your program, a **payload link** will appear in console (example: `https://smee.io/Ab7xK9mNpQr2w`).

> [!WARNING]
> This **payload link** must be pasted in your repository webhook. Otherwise, you will not receive event(s).

##

### Customization

You can also change **types of events**, their **titles** and **descriptions** in a `snitch/snitch.py` file. This is how it looks:

```python
_SAMPLES = {
    "push": {
        "title": "↗ Push from {data[pusher][name]}",
        "desc": "`Commit Messages:`\n{data[head_commit][message]}\n\n`Forced: {data[forced]}`",
    },
    "pull_request": {
        "title": "⤵ {data[pull_request][title]} was *{data[action]}* by {data[sender][login]}",
        "desc": "`Number: {data[number]}`",
    },
    "release": {
        "title": "⬇ {data[release][name]} was *{data[action]}* by {data[release][author][login]}",
        "desc": "`Pre Release: {data[release][prerelease]}`\n`Id: {data[release][id]}`",
    },
    "issues": {
        "title": "⚠ {data[issue][title]} was *{data[action]}* by {data[issue][user][login]}",
        "desc": "`Id: {data[issue][id]}`",
    },
}
```

> [!NOTE]
> To access [event data](https://docs.github.com/en/webhooks/webhook-events-and-payloads) use `{data[...]}`, to go to the next line use `\n`.

## Contribution
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
