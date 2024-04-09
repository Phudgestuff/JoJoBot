import discord
from discord.ext import commands
import cogs.getdata as getdata
from cogs.data.movelist import movelistclass
import math

guilds = [
    690194500039082053,
    940890627221110795,
    939710720227041290
]

class inv(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(guild_ids=guilds)
    async def moveinventory(self, ctx):
        self.users = getdata.Fetch('./cogs/data/users.json').read_info()
        self.standlist = getdata.Fetch('./cogs/data/standlist.json').read_info()
        user = self.users[str(ctx.user.id)]
        movelist = movelistclass(user['level']).movelist
        standid = str(user['stand'])
        stand = self.standlist[standid]
        possiblemoves = user['moves']
        
        movestring = f'    -\n'
        for a in possiblemoves:
            move = movelist[a]
            if a == 0:
                movestring += "**No move selected**\n    -\n"
            else:
                movestring += f'''**Name:{move['name']}**
                Level: {move['level']}
                Attack: { math.floor( (move['attack'][0] + move['attack'][1]) / 2 ) + move['attack'][0] }
                Accuracy: {move['accuracy']}\n    -\n'''

        await ctx.respond(embed=discord.Embed(
            title=f'Selected moves for {stand["name"]}',
            description=movestring,
            color=discord.Colour.dark_teal()
            #footer='*You will unlock more moves as you level up*'
        ))

    @commands.slash_command(guild_ids=guilds)
    async def select(self, ctx, id, slot):

        self.users = getdata.Fetch('./cogs/data/users.json').read_info()
        self.standlist = getdata.Fetch('./cogs/data/standlist.json').read_info()

        standid = str(self.users[str(ctx.user.id)]["stand"])
        try:
            slot = int(slot)-1 #to allow for indexing in the array
            id = int(id) #throws error if not int/float
            if id not in self.standlist[standid]['moves']:
                id/0 #throws error to go to except
        except:
            await ctx.respond('ID must be a valid ID of a move (not the move name) that is available for your stand or ability. See your available moves and their IDs with `/viewmoves`')
            return

        if slot > 3 or slot < 0:
            await ctx.respond('Slot must be a move slot between 1 and 4')
            return
        
        movelist = movelistclass(self.users[str(ctx.user.id)]["level"]).movelist
        
        self.users[str(ctx.user.id)]['moves'][slot] = id
        if movelist[id]["level"] > self.users[str(ctx.user.id)]["level"]:
            await ctx.respond("You aren't a high enough level to access this move")
            return

        await ctx.respond(f'Updated slot {slot + 1} to move {movelist[id]["name"]}')  #updated slot <slot> to move <move name>
        
        getdata.users.update_info(self.users)

def setup(client):
    client.add_cog(inv(client))