import os
import sys
from discordbot.mcplayers import MinecraftServerPlayers
from discordbot.mcserver import MinecraftServerContainer
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

server = MinecraftServerContainer()

bot = DiscordBot(players=players, server=server)
bot.run(DISCORD_BOT_TOKEN)
