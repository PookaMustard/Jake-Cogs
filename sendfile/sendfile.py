import logging
import logging.handlers
import asyncio
import discord
from cogs.utils.settings import Settings
from cogs.utils.dataIO import dataIO
from .utils import checks
from discord.ext import commands

class sendfilecog:
    """Sends files using a command. to send cogs like sendfile do [prefix]sendfile cogs/sendfile.py {optional message}"""

    def __init__(self, bot):
        self.bot = bot
        
    @checks.is_owner()
    @commands.command(aliases=["sf", "sendf", "filesend", "fs"], pass_context=True, description="Usage: [prefix]sendfile [file] {optional message}")
    async def sendfile(self, ctx, file, optionalmessage=""):
        with open(file, 'rb') as j:
            await self.bot.send_file(ctx.message.channel, fp=j, content=optionalmessage)

def setup(bot):
    bot.add_cog(sendfilecog(bot))
