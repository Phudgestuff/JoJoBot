import discord
from discord.ext import commands
import cogs.getdata as getdata
import random
from cogs.data.movelist import movelistclass
import math

guilds = [
    690194500039082053,
    940890627221110795,
    939710720227041290
]

class viewing(commands.Cog):
    def __init__(self, client):

        self.users = getdata.Fetch('./cogs/data/users.json').read_info()
        self.standlist = getdata.Fetch('./cogs/data/standlist.json').read_info() 
        self.client = client

    @commands.slash_command()
    async def status(self, ctx, user: discord.commands.Option(str, "user", required = False, default = '')):
        self.users = getdata.Fetch('./cogs/data/users.json').read_info()
        if user=='':
            user=str(ctx.user.id)
        elif user[:2] != '<@':
            ctx.respond('You must ping a user in `user` section of this command.')
        else:
            user = user[2:len(user)-1]

        userping = f'<@!{user}>'
        username = str(await self.client.fetch_user(int(user)))

        try:
            embed = discord.Embed(
                title=f'User info for {username[:len(username)-2]}',
                description=f'''User: {userping}
                    Health: {self.users[user]["health"]}/{self.users[user]["maxHealth"]}
                    Stand/Ability: {self.standlist[str(self.users[user]["stand"])]["name"]}
                    Type: {self.standlist[str(self.users[user]["stand"])]["type"]}
                    Level: {self.users[user]["level"]}
                    Exp: {self.users[user]["exp"]}/{self.users[user]["reqExp"]}
                    Battle mode: {self.users[user]["battle"]}''',
                color=discord.Colour.green()
            )
        except KeyError:
            embed = discord.Embed(
                title='User has no data in JoJoBot'
            )
        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def viewmoves(self, ctx):
        self.users = getdata.Fetch('./cogs/data/users.json').read_info()
        user = self.users[str(ctx.user.id)]
        movelist = movelistclass(user['level']).movelist
        standid = str(user['stand'])
        stand = self.standlist[standid]
        possiblemoves = stand['moves']
        
        movestring = f'-\n'
        for a in possiblemoves:
            move = movelist[a]
            if move['level'] <= user['level']:
                movestring += f'''**Name: {move['name']}**
                ID: {a}
                Level: {move['level']}
                Attack: { math.floor( (move['attack'][0] + move['attack'][1]) / 2 ) + move['attack'][0] }
                Accuracy: {move['accuracy']}\n-\n'''

        await ctx.respond(embed=discord.Embed(
            title=f'Your moves for {stand["name"]}',
            description=movestring,
            color=discord.Colour.purple()
            #footer='*You will unlock more moves as you level up*'
        ))


def setup(client):
    client.add_cog(viewing(client))