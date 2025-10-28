![banner](/docs/banner.png)

<div align="center">
<h2>
    Application to send GitHub events in a specific Discord channels
</h2>
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

Information about how to create bot and get token can be found [here](https://discordpy.readthedocs.io/en/stable/discord.html)

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

### Customization

You can also change types of events, their titles and descriptions in a `snitch/snitch.py` file. This is how it looks:

```python
_SAMPLES = {
    "push": {
        "title": "↗ push from {data[pusher][name]}",
        "desc": "Commit Message: {data[head_commit][message]}\n\n`Forced: {data[forced]}`"
    },
    "pull_request": {
        "title": "⤵ pull request from {data[sender][name]}",
        "desc":"Action: {data[action]}\n\n`Number: {data[number]}`",
    },
    "release": {
        "title": "⬇ new release from {data[release][author][name]}",
        "desc": "Name: {data[release][name]}\nAction: {data[action]}\n\n`Pre Release: {data[release][prerelease]}`\n`Id: {data[release][id]}`",
    },
    "issues": {
        "username": "⚠ {data[sender][login]}",
        "desc": "Name: {data[issue][title]}\nAuthor: {data[issue][user][login]}\n\n`Id: {data[issue][id]}`"
    }
}
```

> [!NOTE]
> To access [event data](https://docs.github.com/en/webhooks/webhook-events-and-payloads) use `{data[...]}`, to go to the next line use `\n`.

## Contribution
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.