# Minecraft Discord Bot
Discord bot for a private docker hosted minecraft server. This bot currently isn't hosted publicly so you'll need to host it yourself (preferably also in docker).

# Features
* Message a channel whenever someone leaves or joins your server.
* Displaying the number of currently online players in the bots game activity.
* A number of useful commands (!minecraft help):
  * Restarting the server
  * Adding users to the whitelist
  * Listing the online players
  * Sending a message to players on the server

# Requirements
For most of the commands to work you'll need to be running your actual minecraft server in docker in a container called 'mc'.

# Docker
The docker images can be built with this command:
```
docker build -t minecraft-discord-bot:latest .
```

You must provide the following environment variables with the -e flag:
* DISCORD_BOT_TOKEN
* MINECRAFT_HOSTNAME
* GUILD_ID
* CHANNEL_NAME

Most of the commands expect your server to be running in docker with the container name 'mc'.

So if you are running the bot in docker you'll need to mount the docker socket from the host into the bots container (docker in docker! aka dind).

Example docker run command:
```
docker run -e DISCORD_BOT_TOKEN=REPLACE_ME \
    -e MINECRAFT_HOSTNAME=REPLACE_ME \
    -e GUILD_ID=REPLACE_ME \
    -e CHANNEL_NAME=REPLACE_ME \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -it minecraft-discord-bot:latest
```
