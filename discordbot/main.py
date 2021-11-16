import os
import sys
from discordbot.mcplayers import MinecraftServerPlayers
from discordbot.mcserver import MinecraftServerContainer
from discordbot.bot import DiscordBot


# Environment Variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
MINECRAFT_HOSTNAME = os.getenv('MINECRAFT_HOSTNAME')
DOCKER_ENABLED = os.getenv('DOCKER_ENABLED')

try:
	MINECRAFT_PORT = int(os.getenv('MINECRAFT_PORT'))
except ValueError:
	MINECRAFT_PORT = 25565

if DISCORD_BOT_TOKEN is None:
    print('Missing DISCORD_BOT_TOKEN environment variable.')
    sys.exit(1)

if MINECRAFT_HOSTNAME is None:
    print('Missing MINECRAFT_HOSTNAME environment variable.')
    sys.exit(1)

print(f"Player polling will be against {MINECRAFT_HOSTNAME}:{MINECRAFT_PORT}")
players = MinecraftServerPlayers(MINECRAFT_HOSTNAME, MINECRAFT_PORT)
players.start()

container = None
if DOCKER_ENABLED:
	container = MinecraftServerContainer()

bot = DiscordBot(players=players, container=container)

bot.run(DISCORD_BOT_TOKEN)
