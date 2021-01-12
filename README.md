# Minecraft Discord Bot
Small discord bot that is compatible with any minecraft server.

Add to your discord server here:
https://discord.com/api/oauth2/authorize?client_id=798323233274724383&permissions=3072&scope=bot%20applications.commands

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

DOCKER:

docker build -t test:local .
docker run -e DISCORD_BOT_TOKEN=Nzk4MzIzMjMzMjc0NzI0Mzgz.X_zWcg.1gw7Byxw3W2It7uGxM_YdpcLKeg -e MINECRAFT_HOSTNAME=minecraft.joe.carter.sh -e GUILD_ID=264521994496770058 -e CHANNEL_NAME=mc-bot-test-channel -it test:local
