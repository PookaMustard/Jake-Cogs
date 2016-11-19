from discord.ext import commands
from cogs.utils.dataIO import dataIO
import discord
import cogs.utils.checks as checks


class Profile:
    def __init__(self, bot):
        self.bot = bot
        self.things = ['name', 'age', 'gender', 'location', 'description', 'relationship', 'luckynumber']
        try:
            self.db = dataIO.load_json("data/profiles.json")
        except FileNotFoundError:
            self.db = {}

    def save_db(self):
        dataIO.save_json("data/profiles.json", self.db)

    def checkindb(self, id):
        if 'global' in self.db:
            if id in self.db['global']:
                return True
            else:
                self.db['global'][id] = {}
                self.save_db()
                return True
        else:
            self.db['global'] = {}
            self.db['global'][id] = {}
            self.save_db()
            return True

    def checkindbserver(self, userid, serverid):
        if 'servers' in self.db:
            if serverid in self.db['servers']:
                if userid in self.db['servers'][serverid]:
                    return True
                else:
                    self.db['servers'][serverid][userid] = {}
                    self.save_db()
                    return True
            else:
                self.db['servers'][serverid] = {}
                self.db['servers'][serverid][userid] = {}
                self.save_db()
                return True
        else:
            self.db['servers'] = {}
            self.db['servers'][serverid] = {}
            self.db['servers'][serverid][userid] = {}
            self.save_db()
            return True

    def showprofile(self, message, userid, switch):
        serverid = message.server.id
        if switch:
            if 'servers' in self.db:
                if serverid in self.db['servers']:
                    if userid in self.db['servers'][serverid]:
                        return self.db['servers'][serverid][userid]
        if 'global' in self.db:
            if userid in self.db['global']:
                return self.db['global'][userid]
        return 0

    @commands.command(pass_context=True, aliases=['p'])
    async def profile(self, ctx, user: discord.Member=None):
        """Checks for a user's or your own profile."""

        if user is None:
            userid = ctx.message.author.id
        else:
            userid = user.id
        serverid = ctx.message.server.id
        data = self.showprofile(ctx.message, userid, True)
        if data != 0:
            messagetosend = "```\n"
            for thing in self.things:
                if thing == 'luckynumber':
                    thingtitle = 'Lucky Number'
                else:
                    thingtitle = thing
                messagetosend += "{}: {}\n".format(thingtitle.title(), data.get(thing, "Undefined"))
            messagetosend += "```"
            await self.bot.say(messagetosend)
        else:
            await self.bot.say("That user doesn't have a profile.")

    @commands.command(pass_context=True, aliases=['gp'])
    async def profileglobal(self, ctx, user: discord.Member=None):
        """Checks for a user's or your own global profile."""

        if user is None:
            userid = ctx.message.author.id
        else:
            userid = user.id
        data = self.showprofile(ctx.message, userid, False)
        if data != 0:
            messagetosend = "```\n"
            for thing in self.things:
                if thing == 'luckynumber':
                    thingtitle = 'Lucky Number'
                else:
                    thingtitle = thing
                messagetosend += "{}: {}\n".format(thingtitle.title(), self.db['global'][userid].get(thing, "Undefined"))
            messagetosend += "```"
            await self.bot.say(messagetosend)
        else:
            await self.bot.say("That user doesn't have a profile.")

    @commands.command(pass_context=True, aliases=['sp'])
    async def setprofileglobal(self, ctx, thing: str=None, *, value: str=None):
        """Changes your own profile.

           Currently accepted profile entries: name, age, gender, location, description, and luckynumber"""

        if thing is None:
            return await self.bot.say("You haven't provided me a thing to change.")
        thing = thing.lower()
        self.checkindb(ctx.message.author.id)
        if thing in self.things and value is not None:
            self.db['global'][ctx.message.author.id][thing] = value
            self.save_db()
            await self.bot.say("You have set {} to '{}' for yourself.".format(thing.capitalize(), value, ))
        else:
            beep = ""
            for index, potato in enumerate(self.things):
                beep += potato
                if index != len(self.things) - 1:
                    beep += ", "
            await self.bot.say("You need to specify a thing to set, valid things are " + beep + ".")

    @commands.command(pass_context=True, aliases=['sps'])
    async def setprofile(self, ctx, thing: str=None, *, value: str=None):
        """Changes your own profile only on the server this is executed on.

           Currently accepted profile entries: name, age, gender, location, description, and luckynumber"""

        if thing is None:
            return await self.bot.say("You haven't provided me a thing to change.")
        thing = thing.lower()
        userid = ctx.message.author.id
        serverid = ctx.message.server.id
        self.checkindbserver(userid, serverid)
        if thing in self.things and value is not None:
            self.db['servers'][serverid][userid][thing] = value
            self.save_db()
            await self.bot.say("You have set {} to '{}' for yourself.".format(thing.capitalize(), value, ))
        else:
            beep = ""
            for index, potato in enumerate(self.things):
                beep += potato
                if index != len(self.things) - 1:
                    beep += ", "
            await self.bot.say("You need to specify a thing to set, valid things are " + beep + ".")

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def adminsetprofile(self, ctx, user: discord.Member, thing: str=None, *, value: str=None):
        """Changes your own or another user's profile. Administrators only.

           Currently accepted profile entries: name, age, gender, location, description, and luckynumber"""

        if thing is None:
            return await self.bot.say("You haven't provided me a thing to change.")
        thing = thing.lower()
        userid = user.id
        serverid = ctx.message.server.id
        self.checkindbserver(userid, serverid)
        if thing in self.things and value is not None:
            self.db['servers'][serverid][userid][thing] = value
            self.save_db()
            await self.bot.say("You have set {} to '{}' for the user {}.".format(thing.capitalize(), value, user.mention, ))
        else:
            beep = ""
            for index, potato in enumerate(self.things):
                beep += potato
                if index != len(self.things) - 1:
                    beep += ", "
            await self.bot.say("You need to specify a thing to set, valid things are " + beep + ".")


def setup(bot):  # makes sure cog works
    bot.add_cog(Profile(bot))
