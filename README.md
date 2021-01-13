# Minecraft Discord Bot
Small discord bot that is compatible with any minecraft server.

This currently isn't hosted publicly so you'll need to host it yourself, the bot is designed to work with a single discord server.

Features:
* Log to a channel whenever someone leaves or joins your server.

# Docker
The docker images can be built with this command:
```
docker build -t minecraft-discord-bot:latest
```

You must provide the following environment variables with the -e flag:
* DISCORD_BOT_TOKEN
* MINECRAFT_HOSTNAME
* GUILD_ID
* CHANNEL_NAME

# Docker Setup
```
docker build -t minecraft-discord-bot:latest .

docker run -e DISCORD_BOT_TOKEN=${REPLACE_ME} \
    -e MINECRAFT_HOSTNAME=${REPLACE_ME} \
    -e GUILD_ID=${REPLACE_ME} \
    -e CHANNEL_NAME=${REPLACE_ME} \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -it minecraft-discord-bot:latest
```
