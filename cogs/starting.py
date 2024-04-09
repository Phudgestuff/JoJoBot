import discord
from discord.ext import commands
import cogs.getdata as getdata
import random
import cogs.func as func

guilds = [
    690194500039082053,
    940890627221110795,
    939710720227041290
]


class start(commands.Cog):

    def __init__(self, client):

        self.users = getdata.Fetch('./cogs/data/users.json').read_info()
        self.standlist = getdata.Fetch('./cogs/data/standlist.json').read_info() 
        self.client = client

    @commands.slash_command(guild_ids=guilds)
    async def getstand(self, ctx):
        id = str(ctx.user.id)
        self.users = getdata.Fetch('./cogs/data/users.json').read_info()
        if self.users[id]['stand'] != 0:
            await ctx.respond('You already have a stand. You can use `/reset` to reset all your progress, including your stand, exp and moves.')
            return
        
        amntActStands = 0
        for a in self.standlist:
            if '.' in a:
                amntActStands += 1
        standid = random.randint(1, len(self.standlist)-1-amntActStands)
        #standid = 1
        self.users[id]['stand'] = standid
        self.users[id]['level'] = 0
        self.users[id]['exp'] = 0
        self.users[id]['reqExp'] = 15
        embed = discord.Embed(
            title=f'You unlocked {self.standlist[str(standid)]["name"]}',
            description="Level up to unlock moves for this stand",
            color=discord.Colour.purple()
        )
        await ctx.respond(embed=embed)
        getdata.Fetch('./cogs/data/users.json').update_info(self.users)
        self.users = getdata.Fetch('./cogs/data/users.json').read_info()
        print('given stand', self.users[id]['stand'], 'to', ctx.user.name)

    @commands.slash_command(guild_ids=guilds)
    async def reset(self, ctx, confirm):
        if confirm.lower() != 'confirm':
            await ctx.respond('Are you sure? Add `confirm` into the conirm box when inputting this command to reset.')
            return
        reset = self.users[str(ctx.user.id)]['resets']
        reset += 1
        if self.users[str(ctx.user.id)]['resets'] > 4:
            await ctx.respond("You have already reset five times. You must contact <@589489342234492928> if you want to reset again (provide good reason please).")
            return
        self.users = getdata.Fetch('./cogs/data/users.json').read_info()
        
        self.users = func.reset(str(ctx.user.id))
        self.users[str(ctx.user.id)]['resets']=reset

        getdata.users.update_info(self.users)
        print('reset', ctx.user.name)
        await ctx.respond('Reset to level 0')

    @commands.slash_command(guild_ids=guilds)
    async def battlemode(self, ctx):
        self.users = getdata.Fetch('./cogs/data/users.json').read_info()
        self.users[str(ctx.user.id)]['battle'] = not(self.users[str(ctx.user.id)]['battle'])
        await ctx.respond(f'Toggled battle mode to {self.users[str(ctx.user.id)]["battle"]}')

        getdata.users.update_info(self.users)

def setup(client):
    client.add_cog(start(client))
