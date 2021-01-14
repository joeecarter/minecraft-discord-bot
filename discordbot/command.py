from discord.ext import commands


class MinecraftCommand(commands.Cog):

    def __init__(self, players, server):
        self.players = players
        self.server = server

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

    @minecraft.command(help='Says something in game')
    async def say(self, ctx):
        text = remove_prefix(ctx.message.content, '!minecraft say')
        self.server.say(text.strip())

    @minecraft.command(help='Starts a server backup')
    async def backup(self, ctx):
        self.server.start_backup()
        await ctx.send('Backup successfully requested')

    @minecraft.command(help='Restarts the server')
    async def restart(self, ctx):
        self.server.restart_server()
        await ctx.send('Server has been restarted, please give it some time to startup before trying to join.')


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
