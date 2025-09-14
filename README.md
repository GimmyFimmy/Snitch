![alt text](https://github.com/GimmyFimmy/Snitch/blob/dev/docs/banner.png)
```python
# Initialize Snitch library
from snitch import snitch

# Set Discord token (required)
snitch.set_key_value(
    snitch.CacheKeyType.DiscordToken,
    "DISCORD_BOT_TOKEN_HERE",
)

# Set Channel id (required)
snitch.set_key_value(
    snitch.CacheKeyType.PushChannelId,
    "CHANNEL_ID_HERE",
)

# Startup bot
snitch.run()
```