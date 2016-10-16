from discord.ext import commands
from cogs.utils.dataIO import dataIO
import discord
import cogs.utils.checks as checks


class Profile:
    def __init__(self, bot):
        self.bot = bot
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
    async def profile(self, ctx, user:discord.Member=None):
        if user == None:
            id = ctx.message.author.id
        else:
            id = user.id
        if self.checkindb(id):
            await self.bot.say("```Name: {}\nAge: {}\nGender: {}\nLocation: {}\nDescription: {}\nRelationship status: {}```".format(self.db[id].get("name", "unset"), self.db[id].get("age", "unset"), self.db[id].get("gender", "unset"), self.db[id].get("location", "unset"), self.db[id].get("description", "unset"), self.db[id].get("relationship", "unset")))

    @commands.command(pass_context=True)
    async def set(self, ctx, thing:str=None, *, value:str=None):
        self.checkindb(ctx.message.author.id)
        if thing == name or thing == gender or thing == age or thing == description or thing == relationship or thing == location and not value == None:
            self.db[ctx.message.author.id][thing] = value.title()
            self.save_db()
            await self.bot.say("You now have set  {} to {}".format(thing.capitalize(), value))
        elif thing == None:
            await self.bot.say("You need to specify a thing to set, valid things are name, gender, age, description, relationship and location")

def setup(bot): #makes sure cog works
    bot.add_cog(Profile(bot))
