import asyncio
import os
import sys
import discord
from discord.ext import commands
from discordbot.mcplayers import MinecraftServerPlayers

# TODO: Commands...
# from discord.ext import commands
# bot = commands.Bot(command_prefix='$')


class DiscordBot(commands.Bot):

    def __init__(self, players: MinecraftServerPlayers):
        self.loop = asyncio.get_event_loop()
        super(DiscordBot, self).__init__(loop=self.loop, status=discord.Status.online, command_prefix="!")

        self.players = players
        self.guild = None
        self.channel = None

        self.add_command(self.on_minecraft_command)

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
        self.__init_players()
        await self.__update_presence()


    async def on_player_join(self, player):
        await self.channel.send(f'{player} joined the server')
        await self.__update_presence()

    async def on_player_leave(self, player):
        await self.channel.send(f'{player} left the server')
        await self.__update_presence()

    @staticmethod
    @commands.command(name='minecraft', help='Collection of commands for interacting with the minecraft server. Use !minecraft help for more info.')
    async def on_minecraft_command(ctx, sub_command):
        if sub_command == 'help':
            await ctx.send('Available commands:')
            await ctx.send('* !minecraft hello:  Say hello to your friendly neighbourhood bot!')
        elif sub_command == 'hello':
            await ctx.send('Hello there :wave:')
        elif sub_command == 'restart':
            await ctx.send('WIP')
        else:
            await ctx.send(f'Unknown sub-command \'{sub_command}\', type !minecraft help for a list of available subcommands.')

    def find_channel(self, name):
        return discord.utils.find(lambda channel: channel.name == name, self.guild.channels)

    async def __update_presence(self):
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

    def __init_players(self):
        loop = self.loop

        def player_join(player):
            loop.create_task(self.on_player_join(player))

        def player_leave(player):
            loop.create_task(self.on_player_leave(player))

        self.players.on_player_join(player_join)
        self.players.on_player_leave(player_leave)

    @staticmethod
    def load_channel_name():
        channel_name = os.getenv('CHANNEL_NAME')
        if channel_name is None:  # TODO: This sucks...
            print('Missing CHANNEL_NAME environment variable.')
            sys.exit(2)
        return channel_name

    @staticmethod
    def load_guild_id():
        guild_id = int(os.getenv('GUILD_ID')) if os.getenv('GUILD_ID') else None
        if guild_id is None:  # TODO: This sucks...
            print('Missing GUILD_ID environment variable.')
            sys.exit(2)
        return guild_id
