from discord.ext import commands
from cogs.utils.dataIO import dataIO
import discord
from __main__ import send_cmd_help


class Cookies:
    def __init__(self, bot):
        self.bot = bot
        try:
            self.db = dataIO.load_json("data/cookies.json")  # load cookie db
        except FileNotFoundError:
            self.db = {}

    def save_db(self):
        dataIO.save_json("data/cookies.json", self.db)

    @commands.group(no_pm=True, invoke_without_command=True, pass_context=True)
    async def cookies(self, ctx):
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @cookies.command(pass_context=True)
    async def createaccount(self, ctx):
        """Creates an account in the cookie bank!"""
        if ctx.message.server.id not in self.db:
            self.db[ctx.message.server.id] = {}  # if the server isnt in db it will add server
        if ctx.message.author.id not in self.db[ctx.message.server.id]:
            self.db[ctx.message.server.id][ctx.message.author.id] = 5  # starting balance of 5
            self.save_db()  # save
            await self.bot.say("You're now in the :cookie: database.")
        else:
            await self.bot.say("You can't have two accounts!")

    @cookies.command(pass_context=True)
    async def balance(self, ctx, *, user: discord.Member= None):
        """Checks how many cookies you have in the cookie bank!"""
        if user is None:  # if there is no user being mentioned it willview your balance
            user = ctx.message.author
        if user.id in self.db[ctx.message.server.id]:
            userdb = self.db[ctx.message.server.id][user.id]
            await self.bot.say('User {}  Has: {} :cookie:\'s.'.format(user.name, userdb))
        else:
            await self.bot.say('Create a account with [prefix]cookies createaccount')  # says you need a account

    @cookies.command(pass_context=True)
    async def give(self, ctx, user: discord.Member=None, amount: int= None):
        """Gives cookies to someone!"""
        if user is None or amount is None:
            await self.bot.say('Correct usage is [prefix]cookies give <user> <amount>')
        else:
            userid = user.id
            amount = abs(amount)
            if ctx.message.author.id in self.db[ctx.message.server.id] and userid in self.db[ctx.message.server.id]:
                if int(amount) <= self.db[ctx.message.server.id][ctx.message.author.id]:
                    self.db[ctx.message.server.id][ctx.message.author.id] -= amount
                    self.db[ctx.message.server.id][userid] += amount
                    await self.bot.say('Done!')
                    self.save_db()
                else:
                    await self.bot.say('You don\'t have enough :cookie:\'s to give')
            else:
                messagetosay = """Either you or the receiver don\'t have a account,
                                  to create a account do [prefix]cookies createaccount"""
                await self.bot.say(messagetosay)

    @cookies.command(pass_context=True)
    async def eat(self, ctx):
        """Eat one of your cookies!"""
        if 1 <= self.db[ctx.message.server.id][ctx.message.author.id]:
            self.db[ctx.message.server.id][ctx.message.author.id] -= 1  # it will take a cookie from you
            await self.bot.say('You have eaten a :cookie:!')  # and eat said cookie
        else:
            await self.bot.say("You don't have enough :cookie:'s!")

    @cookies.command(pass_context=True)
    async def award(self, ctx, user: discord.Member=None, amount: int=None):
        """Users with the CookieGiver role can award cookies to good memebers."""
        if ctx.message.author.id == "207896356537368577" or "CookieGiver" in [r.name for r in ctx.message.author.roles]:
            if user is None or amount is None:  # gives help
                await self.bot.say('Correct usage is [prefix]award [user] [amount]')
            else:
                if user.id == ctx.message.author.id:  # person cant award cookies to themself
                    await self.bot.say("Don't try to give cookies to yourself...")
                else:
                    userid = user.id
                    if userid in self.db[ctx.message.server.id]:
                        self.db[ctx.message.server.id][userid] += amount  # give them cookies
                        await self.bot.say('Done!')
                        self.save_db()
                    else:
                        await self.bot.say("User doesnt have a cookie account!")
        else:
            await self.bot.say("You need the CookieGiver role to use this command!")


def setup(bot):
    bot.add_cog(Cookies(bot))
