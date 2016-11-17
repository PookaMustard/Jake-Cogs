from discord.ext import commands
from cogs.utils.dataIO import dataIO
import discord
import cogs.utils.checks as checks


class Profile:
    def __init__(self, bot):
        self.bot = bot
        self.things = ['name', 'age', 'gender', 'location', 'description', 'relationship']
        try:
            self.db = dataIO.load_json("data/profiles.json")
        except FileNotFoundError:
            self.db = {}

    def save_db(self):
        dataIO.save_json("data/profiles.json", self.db)

    def checkindb(self, id):
        if id in self.db:
            return True
        else:
            self.db[id] = {}
            self.save_db()
            return True

    @commands.command(pass_context=True)
    async def profile(self, ctx, user: discord.Member=None):
        if user is None:
            id = ctx.message.author.id
        else:
            id = user.id
        if self.checkindb(id):
            messagetosend = ""
            for thing in self.things:
                messagetosend += "{}: {}\n".format(thing.capitialize(), self.db[id].get(thing, "Undefined"))
            await self.bot.say(messagetosend)

    @commands.command(pass_context=True)
    async def setprofile(self, ctx, thing: str=None, *, value: str=None):
        self.checkindb(ctx.message.author.id)
        if thing in self.things and value is not None:
            self.db[ctx.message.author.id][thing] = value
            self.save_db()
            await self.bot.say("You have set {} to '{}' for yourself.".format(thing.capitalize(), value, ))
        elif thing is None:
            await self.bot.say("You need to specify a thing to set, valid things are" + self.things)

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def adminsetprofile(self, ctx, user: discord.Member, thing: str=None, *, value: str=None):
        id = user.id
        if thing in self.things and value is not None:
            self.db[id][thing] = value
            self.save_db()
            await self.bot.say("Done!")
        elif thing is None:
            await self.bot.say("You need to specify a thing to set, valid things are " + self.things)


def setup(bot):  # makes sure cog works
    bot.add_cog(Profile(bot))
