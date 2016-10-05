from discord.ext import commands
from cogs.utils.dataIO import dataIO
import discord
import cogs.utils.checks as checks

class Cookies: #makes the cookies class
    def __init__(self, bot):
        self.bot = bot #so you can do bot stuff and things
        try:
            self.db = dataIO.load_json("data/cookies.json") #load cookie db
        except FileNotFoundError:
            self.db = {} #if not found make it blank because it will make a new file anyway

    def save_db(self): #save db
        dataIO.save_json("data/cookies.json", self.db)

    @commands.group(no_pm=True, invoke_without_command=True) #creates cookie command group
    async def cookies(self):
        await self.bot.say('All cookie commands are used like |cookie {subthing here} Here are a list of the subwhatevers: Createaccount, balance and give.') #gives help

    @cookies.command(pass_context=True) #defines the create account command in the cookie subset
    async def createaccount(self, ctx):
        if ctx.message.server.id not in self.db:
            self.db[ctx.message.server.id] = {} #if the server isnt in db (failsafe cause when it joins a server it auto does that anyway) it will add the server
        if ctx.message.author.id not in self.db[ctx.message.server.id]: #if the user isnt in the db then
            self.db[ctx.message.server.id][ctx.message.author.id] = 5 #gives them a starting balance of 5
            self.save_db() #saves db
            await self.bot.say("You're now in the cookie database.") #says stuff
        else:
            await self.bot.say("You can't have two accounts!") #and things

    @cookies.command(pass_context=True) #defines the balance command in the cookies subset
    async def balance(self, ctx, *, user:discord.Member= None):
        if user == None: #if there is no user being mentioned it will think you want to view your balance
            user = ctx.message.author #makes the user you
        if user.id in self.db[ctx.message.server.id]: #if the user is in the db
            await self.bot.say('User {}  Has: {} cookies.'.format(user.name, str(self.db[ctx.message.server.id][user.id]))) #says how many cookies they have
        else: #else
            await self.bot.say('Create a account with |createaccount') #says you need a account

    @cookies.command(pass_context=True) #defines the give command in the cookie subset
    async def give(self, ctx, user:discord.Member=None, amount:int= None):
        if user == None: #if there is no user it will give help on how to use the command
            await self.bot.say('Correct usage is (prefix)give @user howmany')
        else: #when if there is then
            userid = user.id #the users id of the person you give it too will be called userid
            if ctx.message.author.id in self.db[ctx.message.server.id] and userid in self.db[ctx.message.server.id]: #if they are both in db
                if int(amount) <= self.db[ctx.message.server.id][ctx.message.author.id]: #and if the ammount you want to give you have in your balance then
                    self.db[ctx.message.server.id][ctx.message.author.id] = self.db[ctx.message.server.id][ctx.message.author.id] - int(amount) #will subtract the cookies from the users account
                    self.db[ctx.message.server.id][userid] = int(amount) + self.db[ctx.message.server.id][userid] #and will add to the reciver
                    await self.bot.say('Done!') #says it did it
                    self.save_db() #saves db
                else: #however if they dont have enough cookies to give then
                    await self.bot.say('You don\'t have enough cookies to give') #duur it says you dont hav enough cookies, dont try to give stuff you dont have hmm i might add a debt feature or cookie loans later
            else: #if one or both of you are not in the db then
                await self.bot.say('Either you or the receiver don\'t have a account, to create a account do |createaccount') #will say you dont have a account

    @cookies.command(pass_context=True) #adds a eat command
    async def eat(self, ctx):
        if 1 <= self.db[ctx.message.server.id][ctx.message.author.id]: #if you have more or = to 1 cookie then
            self.db[ctx.message.server.id][ctx.message.author.id] = self.db[ctx.message.server.id][ctx.message.author.id] - 1 #it will take a cookie from you
            await self.bot.say('You have eaten a cookie!') #and eat said cookie
        else: #but if you dont have enough cookies
            await self.bot.say("You don't have enough cookies!") #it will say it

def setup(bot): #makes sure cog works
    bot.add_cog(Cookies(bot))
