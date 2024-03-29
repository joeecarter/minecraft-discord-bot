from discord.ext import commands


class MinecraftCommand(commands.Cog):

    def __init__(self, players, container):
        self.players = players
        self.container = container

    @commands.group(pass_context=True)
    async def minecraft(self, ctx):
        pass

    # TODO: Unfortunately I couldn't get the built in help command to work with @commands.group
    @minecraft.command(help='Prints out the available commands')
    async def help(self, ctx):
        await ctx.send('Available commands: hello, players, say <message>, backup, restart, whitelist')

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
        self.container.say(text.strip())

    @minecraft.command(help='Starts a server backup')
    async def backup(self, ctx):
        self.container.start_backup()
        await ctx.send('Backup successfully requested')

    @minecraft.command(help='Restarts the server')
    async def restart(self, ctx):
        self.container.restart_server()
        await ctx.send('Server has been restarted, please give it some time to startup before trying to join.')

    @minecraft.command(help='Adds a username to the whitelist')
    async def whitelist(self, ctx, username):
        self.container.whitelist_add(username)
        await ctx.send(f'Added \'{username}\' to the whitelist')


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
