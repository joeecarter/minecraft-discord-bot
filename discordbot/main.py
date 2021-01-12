import asyncio
import os
import sys
import bot

from discordbot.mcplayers import MinecraftServerPlayers
from discordbot.bot import DiscordBot


# Environment Variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
MINECRAFT_HOSTNAME = os.getenv('MINECRAFT_HOSTNAME')

if DISCORD_BOT_TOKEN is None:
    print('Missing DISCORD_BOT_TOKEN environment variable.')
    sys.exit(1)

if MINECRAFT_HOSTNAME is None:
    print('Missing MINECRAFT_HOSTNAME environment variable.')
    sys.exit(1)

players = MinecraftServerPlayers(MINECRAFT_HOSTNAME)
players.start()

client = DiscordBot(players=players)

client.run(DISCORD_BOT_TOKEN)
