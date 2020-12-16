import os
import time
import requests
from mcstatus import MinecraftServer

hostname = os.environ.get('MINECRAFT_HOSTNAME')

if hostname == None:
	print('ERROR: Missing MINECRAFT_HOSTNAME environemnt variable')
	os._exit(0)

server = MinecraftServer(hostname)

discordWebhook = os.environ.get('DISCORD_WEBHOOK')

def fetch_online_players():
	status = server.status()
	players = status.players.sample
	
	if players == None:
		return []
	
	return list(map(lambda player: player.name, players))

def diff(original, changed):
	diff = []
	for x in original:
		if x not in changed:
			diff.append(x)
	return diff

def discordMessage(message):
	if discordWebhook == None:
		return
	requests.post(discordWebhook, { 'username': 'MC Status', 'content': message })	


players = fetch_online_players()

while True:
	time.sleep(60)
	newPlayers = fetch_online_players()
	
	left = diff(players, newPlayers)
	joined = diff(newPlayers, players)
	
	players = newPlayers

	for player in joined:
		msg = '{0} joined the server'.format(player)
		print(msg)
		discordMessage(msg)

	for player in left:
		msg = '{0} left the server'.format(player)
		print(msg)
		discordMessage(msg)
