import asyncio
import os
import sys
import time
import discord
from discord.ext import commands
from discordbot.command import MinecraftCommand
from signal import SIGINT, SIGTERM


class DiscordBot(commands.Bot):

    def __init__(self, players, server):
        self.loop = asyncio.get_event_loop()
        super(DiscordBot, self).__init__(loop=self.loop, status=discord.Status.online, command_prefix="!")

        self.players = players
        self.guild = None
        self.channel = None

        self.add_cog(MinecraftCommand(players, server))

    async def on_message(self, message):
        await self.process_commands(message)

    async def on_ready(self):
        guild_id = self.load_guild_id()
        channel_name = self.load_channel_name()

        if guild_id is None:
            await self.__print_guild_id_prompt()

        self.guild = self.get_guild(guild_id)
        if self.guild is None:
            await self.__print_guild_id_prompt()

        print('\nChannels:')
        for channel in self.guild.channels:
            print(f'* {channel.name}')
        print('\n')

        self.channel = self.find_channel(channel_name)
        if self.channel is None:
            print(f'Invalid channel #{channel_name}')
            sys.exit(1)

        print(f'Leave/join messages will be posted to #{self.channel.name}')
        self.__init_player_events()
        self.__init_signal_handler_events()
        await self.update_presence()

    async def on_player_join(self, player):
        await self.channel.send(f'{player} joined the server')
        await self.update_presence()

    async def on_player_leave(self, player):
        await self.channel.send(f'{player} left the server')
        await self.update_presence()

    def on_stop_signal(self):
        self.send_message_sync('Bot is being redeployed (or something has gone very wrong)')
        time.sleep(1)
        sys.exit(0)

    async def send_message(self, message):
        await self.channel.send(message)

    def send_message_sync(self, message):
        self.loop.create_task(self.send_message(message))

    def find_channel(self, name):
        return discord.utils.find(lambda channel: channel.name == name, self.guild.channels)

    async def update_presence(self):
        players = self.players.get()
        game = discord.Game(f'{len(players)} players online')
        await self.change_presence(activity=game)

    async def __print_guild_id_prompt(self):
        print('The value of the GUILD_ID environment variable is missing or invalid.')
        print('Please set it to one of the following and run the container again:')
        for guild in self.guilds:
            print(f'*  {guild.name} (id: {guild.id})\n')

        self.clear()
        await self.close()

    def __init_player_events(self):
        loop = self.loop

        def player_join(player):
            loop.create_task(self.on_player_join(player))

        def player_leave(player):
            loop.create_task(self.on_player_leave(player))

        self.players.on_player_join(player_join)
        self.players.on_player_leave(player_leave)

    def __init_signal_handler_events(self):
        self.loop.add_signal_handler(SIGINT, self.on_stop_signal)
        self.loop.add_signal_handler(SIGTERM, self.on_stop_signal)

    @staticmethod
    def load_channel_name():
        channel_name = os.getenv('CHANNEL_NAME')
        if channel_name is None:
            print('Missing CHANNEL_NAME environment variable.')
            sys.exit(2)
        return channel_name

    @staticmethod
    def load_guild_id():
        guild_id = int(os.getenv('GUILD_ID')) if os.getenv('GUILD_ID') else None
        if guild_id is None:
            print('Missing GUILD_ID environment variable.')
            sys.exit(2)
        return guild_id
