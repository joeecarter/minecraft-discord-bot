from discord.ext import commands


class MinecraftCommand(commands.Cog):

    def __init__(self, players):
        self.players = players

    @commands.group(pass_context=True)
    async def minecraft(self, ctx):
        pass

    @minecraft.command(help='Says hello to you')
    async def hello(self, ctx):
        await ctx.send('Hello there :wave:')

    @minecraft.command(help='Lists the currently online players')
    async def players(self, ctx):
        players = self.players.get()
        if len(players) > 0:
            await ctx.send('Online players: ' + ', '.join(players))
        else:
            await ctx.send('No players are online')
