# Initialize Snitch library
from snitch import snitch

# Set Discord token (required)
snitch.set_key_value(
    snitch.CacheKeyType.DiscordToken,
    "DISCORD_BOT_TOKEN_HERE", # <- Example: "MTEyMzQ1Njc4OTExMjM0NTY3ODkw.ABCdef.ghIjKLmnOpQrStUvWxYz"
)

# Set Channel id (required)
snitch.set_key_value(
    snitch.CacheKeyType.PushChannelId, # <- You can select any other available CacheKeyType
    "CHANNEL_ID_HERE", # <- Example: "1725894631057892345"
)

# Startup bot
snitch.run()