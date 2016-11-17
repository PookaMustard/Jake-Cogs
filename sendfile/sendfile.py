from .utils import checks
from discord.ext import commands


class sendfilecog:
    """Sends files using a command.
    to send cogs like sendfile do:
    [prefix]sendfile cogs/sendfile.py {optional message}"""

    def __init__(self, bot):
        self.bot = bot
        self.aliases = ["sf", "sendf", "filesend", "fs"]
        self.help = "Usage: [prefix]sendfile [file] {optional message}"

    @checks.is_owner()
    @commands.command(aliases=self.aliases, pass_context=True, description=self.help)
    async def sendfile(self, ctx, file, optionalmessage=""):
        with open(file, 'rb') as j:
            await self.bot.send_file(ctx.message.channel, fp=j, content=optionalmessage)

def setup(bot):
    bot.add_cog(sendfilecog(bot))
