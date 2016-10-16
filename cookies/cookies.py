from discord.ext import commands
from cogs.utils.dataIO import dataIO
import discord
import cogs.utils.checks as checks
from __main__ import send_cmd_help

class Cookies: #makes the cookies class
    def __init__(self, bot):
        self.bot = bot #so you can do bot stuff and things
        try:
            self.db = dataIO.load_json("data/cookies.json") #load cookie db
        except FileNotFoundError:
            self.db = {} #if not found make it blank because it will make a new file anyway

    def save_db(self): #save db
        dataIO.save_json("data/cookies.json", self.db)

    @commands.group(no_pm=True, invoke_without_command=True, pass_context=True) #creates cookie command group
    async def cookies(self, ctx):
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @cookies.command(pass_context=True) #defines the create account command in the cookie subset
    async def createaccount(self, ctx):
        if ctx.message.server.id not in self.db:
            self.db[ctx.message.server.id] = {} #if the server isnt in db (failsafe cause when it joins a server it auto does that anyway) it will add the server
        if ctx.message.author.id not in self.db[ctx.message.server.id]: #if the user isnt in the db then
            self.db[ctx.message.server.id][ctx.message.author.id] = 5 #gives them a starting balance of 5
            self.save_db() #saves db
            await self.bot.say("You're now in the :cookie: database.") #says stuff
        else:
            await self.bot.say("You can't have two accounts!") #and things

    @cookies.command(pass_context=True) #defines the balance command in the cookies subset
    async def balance(self, ctx, *, user:discord.Member= None):
        if user == None: #if there is no user being mentioned it will think you want to view your balance
            user = ctx.message.author #makes the user you
        if user.id in self.db[ctx.message.server.id]: #if the user is in the db
            await self.bot.say('User {}  Has: {} :cookie:\'s.'.format(user.name, str(self.db[ctx.message.server.id][user.id]))) #says how many cookies they have
        else: #else
            await self.bot.say('Create a account with |createaccount') #says you need a account

    @cookies.command(pass_context=True) #defines the give command in the cookie subset
    async def give(self, ctx, user:discord.Member=None, amount:int= None):
        if user == None: #if there is no user it will give help on how to use the command
            await self.bot.say('Correct usage is [prefix]cookies give <user> <amount>')
        else: #when if there is then
            userid = user.id #the users id of the person you give it too will be called userid
            if ctx.message.author.id in self.db[ctx.message.server.id] and userid in self.db[ctx.message.server.id]: #if they are both in db
                if int(amount) <= self.db[ctx.message.server.id][ctx.message.author.id]: #and if the ammount you want to give you have in your balance then
                    self.db[ctx.message.server.id][ctx.message.author.id] = self.db[ctx.message.server.id][ctx.message.author.id] - int(amount) #will subtract the cookies from the users account
                    self.db[ctx.message.server.id][userid] = int(amount) + self.db[ctx.message.server.id][userid] #and will add to the reciver
                    await self.bot.say('Done!') #says it did it
                    self.save_db() #saves db
                else: #however if they dont have enough cookies to give then
                    await self.bot.say('You don\'t have enough :cookie:\'s to give') #duur it says you dont hav enough cookies, dont try to give stuff you dont have hmm i might add a debt feature or cookie loans later
            else: #if one or both of you are not in the db then
                await self.bot.say('Either you or the receiver don\'t have a account, to create a account do [prefix]createaccount') #will say you dont have a account

    @cookies.command(pass_context=True) #adds a eat command
    async def eat(self, ctx):
        if 1 <= self.db[ctx.message.server.id][ctx.message.author.id]: #if you have more or = to 1 cookie then
            self.db[ctx.message.server.id][ctx.message.author.id] = self.db[ctx.message.server.id][ctx.message.author.id] - 1 #it will take a cookie from you
            await self.bot.say('You have eaten a :cookie:!') #and eat said cookie
        else: #but if you dont have enough cookies
            await self.bot.say("You don't have enough :cookie:'s!") #it will say it
"""
    #needs a check oto make sure only people with cookie giver role can use it, will be done before github update
    @cookies.command(pass_context=True)
    async def award(self, ctx, user:discord.Member=None, amount:int=None):
        if user == None: #if there is no user it will give help on how to use the command
            await self.bot.say('Correct usage is [prefix]award give <user> <amount>')
        if user.id == ctx.message.author.id: #to make sure person cant awward cookies to themself
            await self.bot.say("Don't try to give cookies to yourself...")
        else:
            userid = user.id #the users id of the person you award cookies to
            if userid in self.db[ctx.message.server.id]: #if person is in db
                self.db[ctx.message.server.id][ctx.message.author.id] = self.db[ctx.message.server.id][ctx.message.author.id] + int(amount) #give them cookies
                await self.bot.say('Done!') #says it did it
                self.save_db() #saves db
            else:
                await self.bot.say("User doesnt have a cookie account!") #says error cause user isnt in db or cause jake did a derp
"""
def setup(bot): #makes sure cog works
    bot.add_cog(Cookies(bot))
