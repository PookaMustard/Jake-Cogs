from discord.ext import commands
from cogs.utils.dataIO import dataIO
import discord
import cogs.utils.checks as checks


class Profile:

    def __init__(self, bot):
        self.bot = bot
        self.things = ['name', 'age', 'gender', 'location',
                       'description', 'relationship', 'luckynumber']
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
        item = ''
        itemslist = {}
        serverid = message.server.id
        if switch:
            if 'servers' in self.db:
                if serverid in self.db['servers']:
                    if userid in self.db['servers'][serverid]:
                        for a in self.things:
                            if a not in self.db['servers'][serverid][userid]:
                                item = self.getglobalitem(userid, a)
                                itemslist[a] = item
                            else:
                                itemslist[a] = self.db['servers'][
                                    serverid][userid][a]
                        return itemslist, False
        if 'global' in self.db:
            if userid in self.db['global']:
                return self.db['global'][userid], True
        return 0, False

    def getglobalitem(self, userid, a):
        if 'global' in self.db:
            if userid in self.db['global']:
                if a in self.db['global'][userid]:
                    b = str(self.db['global'][userid][a]) + " (Global)"
                    return b
        return 'Undefined'

    @commands.command(pass_context=True, aliases=['p'])
    async def profile(self, ctx, user: discord.Member=None):
        """Checks for a user's or your own profile."""

        if user is None:
            userid = ctx.message.author.id
        else:
            userid = user.id
        data, globalch = self.showprofile(ctx.message, userid, True)
        if data != 0:
            if globalch:
                messagetosend = "(Derived from global profile)\n```\n"
            else:
                messagetosend = "```\n"
            for thing in self.things:
                if thing == 'luckynumber':
                    thingtitle = 'Lucky Number'
                else:
                    thingtitle = thing
                messagetosend += "{}: {}\n".format(
                    thingtitle.title(), data.get(thing, "Undefined"))
            messagetosend += "```"
            await self.bot.say(messagetosend)
        else:
            await self.bot.say("That user doesn't have a profile.")

    @commands.command(pass_context=True, aliases=['gp', 'pg'])
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
                messagetosend += "{}: {}\n".format(
                    thingtitle.title(), self.db['global'][userid].get
                    (thing, "Undefined"))
            messagetosend += "```"
            await self.bot.say(messagetosend)
        else:
            await self.bot.say("That user doesn't have a profile.")

    @commands.command(pass_context=True)
    async def clearprofile(self, ctx, thing: str=None):
        """Clears a server profile entry or the entire server profile.
        Leaving the thing parameter blank will CLEAR YOUR ENTIRE PROFILE,
        be careful."""

        userid = ctx.message.author.id
        serverid = ctx.message.server.id
        if 'servers' in self.db:
            if serverid in self.db['servers']:
                if userid in self.db['servers'][serverid]:
                    if thing is None:
                        await self.bot.say("Are you sure you want to " +
                                           "clear your entire server " +
                                           "profile? Say `Delete " +
                                           "profile` to confirm.")
                        rp = await self.bot.wait_for_message(
                           author=ctx.message.author)
                        if rp.content.lower() == 'delete profile':
                            del self.db['servers'][serverid][userid]
                            self.save_db()
                            await self.bot.say(
                                "Your entire server profile has been deleted.")
                        else:
                            return await self.bot.say("Operation cancelled.")
                    elif thing not in self.things:
                        return await self.bot.say("No such entry to delete.")
                    else:
                        thingcheck = thing
                        if thingcheck == 'luckynumber':
                            thingcheck = 'lucky number'
                        if thing not in self.db['servers'][serverid][userid]:
                            return await self.bot.say(
                                "Your server profile does not have a {} " +
                                "entry to delete.".format(thingcheck))
                        if len(self.db['servers'][serverid][userid]) == 1:
                            del self.db['servers'][serverid][userid]
                        else:
                            del self.db['servers'][serverid][userid][thing]
                        await self.bot.say(
                            "Your server profile's {} " +
                            "has been deleted.".format(
                                thingcheck))
                        self.save_db()
                    return
        return await self.bot.say("You do not have a profile on this server.")

    @commands.command(pass_context=True)
    async def clearprofileglobal(self, ctx, thing: str=None):
        """Clears a global profile entry or the entire global profile.
        Leaving the thing parameter blank will CLEAR YOUR ENTIRE PROFILE,
        be careful."""

        userid = ctx.message.author.id
        if 'global' in self.db:
            if userid in self.db['global']:
                if thing is None:
                    await self.bot.say(
                        "Are you sure you want to clear your entire " +
                        "global profile? Say `Delete profile` to confirm.")
                    rp = await self.bot.wait_for_message(
                                                author=ctx.message.author)
                    if rp.content.lower() == 'delete profile':
                        del self.db['global'][userid]
                        await self.bot.say(
                            "Your entire global profile has been deleted.")
                    else:
                        return await self.bot.say("Operation cancelled.")
                elif thing not in self.things:
                    return await self.bot.say("No such entry to delete.")
                else:
                    thingcheck = thing
                    if thingcheck == 'luckynumber':
                        thingcheck = 'lucky number'
                    if thing not in self.db['global'][userid]:
                        return await self.bot.say(
                            "Your global profile does not " +
                            "have a {} entry to delete.".format(thingcheck))
                    del self.db['global'][userid][thing]
                    if len(self.db['global'][userid]) == 0:
                        del self.db['global'][userid]
                    await self.bot.say(
                        "Your global profile's {} has been deleted. \
                        ".format(thingcheck))
                self.save_db()
                return
        return await self.bot.say("You do not have a global profile.")

    @commands.command(pass_context=True, aliases=['spg', 'sg'])
    async def setprofileglobal(self, ctx, thing: str=None, *, value: str=None):
        """Changes your own profile.

           Currently accepted profile entries: name, age, gender,
           location, description, and luckynumber"""

        if thing is None:
            return await self.bot.say(
                "You haven't provided me a thing to change.")
        thing = thing.lower()
        self.checkindb(ctx.message.author.id)
        if thing in self.things and value is not None:
            self.db['global'][ctx.message.author.id][thing] = value
            self.save_db()
            await self.bot.say(
                "You have set {} to '{}' for yourself.".format(
                    thing.capitalize(), value, ))
        else:
            beep = ""
            for index, potato in enumerate(self.things):
                beep += potato
                if index != len(self.things) - 1:
                    beep += ", "
            await self.bot.say(
                "You need to specify a thing to set, valid things are " +
                beep + ".")

    @commands.command(pass_context=True, aliases=['sp'])
    async def setprofile(self, ctx, thing: str=None, *, value: str=None):
        """Changes your own profile only on the server this is executed on.

           Currently accepted profile entries: name, age, gender, location,
           description, and luckynumber"""

        if thing is None:
            return await self.bot.say(
                "You haven't provided me a thing to change.")
        thing = thing.lower()
        userid = ctx.message.author.id
        serverid = ctx.message.server.id
        if value is None:
            return await self.bot.say("No value given.")
        self.checkindbserver(userid, serverid)
        if thing in self.things:
            self.db['servers'][serverid][userid][thing] = value
            self.save_db()
            await self.bot.say(
                "You have set {} to '{}' for yourself.".format(
                    thing.capitalize(), value, ))
        else:
            beep = ""
            for index, potato in enumerate(self.things):
                beep += potato
                if index != len(self.things) - 1:
                    beep += ", "
            await self.bot.say(
                "You need to specify a thing to set, valid things are " +
                beep + ".")

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def adminsetprofile(self, ctx, user: discord.Member,
                              thing: str=None, *, value: str=None):
        """Changes your own or another user's profile. Administrators only.

           Currently accepted profile entries: name, age, gender, location,
           description, and luckynumber"""

        if thing is None:
            return await self.bot.say(
                "You haven't provided me a thing to change.")
        thing = thing.lower()
        userid = user.id
        serverid = ctx.message.server.id
        if value is None:
            return await self.bot.say("No value given.")
        self.checkindbserver(userid, serverid)
        if thing in self.things and value is not None:
            self.db['servers'][serverid][userid][thing] = value
            self.save_db()
            await self.bot.say(
                "You have set {} to '{}' for the user {}.".format(
                    thing.capitalize(), value, user.mention, ))
        else:
            beep = ""
            for index, potato in enumerate(self.things):
                beep += potato
                if index != len(self.things) - 1:
                    beep += ", "
            await self.bot.say(
                "You need to specify a thing to set, valid things are " +
                beep + ".")


def setup(bot):  # makes sure cog works
    bot.add_cog(Profile(bot))
