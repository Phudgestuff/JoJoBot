import discord
from discord.ext import commands
import cogs.getdata as getdata
from cogs.data.movelist import movelistclass
import cogs.func as func
#import cogs.data.movefunctions

guilds = [
    690194500039082053,
    940890627221110795,
    939710720227041290
]

class battle(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(guild_ids=guilds)
    async def move(self, ctx, slot, target):

        try:
            slot = int(slot)-1 #to allow for indexing in the array
        except:
            await ctx.respond('ID must be a valid ID of a move (not the move name) that is available for your stand or ability. See your available moves and their IDs with `/viewmoves`')
            return

        if slot > 3 or slot < 0:
            await ctx.respond('Slot must be a move slot between 1 and 4')
            return
        
        self.users = getdata.Fetch('./cogs/data/users.json').read_info()
        if target[:2] != '<@':
            await ctx.respond('You must ping a user in `target` section of this command.')
            return
        
        user = target[2:len(target)-1]

        if self.users[user]['battle'] == False:
            await ctx.respond(f'{target} has battle mode turned off.')
            return
        

        # move code actually starts here all above is boilerplate

        username = str(await self.client.fetch_user(int(user)))
        uid = str(ctx.user.id)
        level = self.users[uid]['level']

        self.users[uid]['lastMove'] = self.users[uid]['moves'][slot]
        #lastMove = self.users[uid]['lastMove']

        #movelist = movelistclass(level).movelist
        moveid = self.users[uid]['moves'][slot]
        self.standlist = getdata.Fetch('./cogs/data/standlist.json').read_info()

        #move = movelist[moveid]
        if moveid == 0:
            await ctx.respond("No move selected")
            return
        
        self.users = getdata.Fetch('./cogs/data/users.json').read_info()
        ml = movelistclass(level, self.users[uid]['lastMove'], self.users[uid]['accMult'], self.users[uid]['damageMult']).movelist[moveid]
        
        moveresult = ml['method'](
            self=ml['class'],
            level=level, 
            damage=ml['attack'],
            accuracy=ml['accuracy'],
            lastmove=self.users[uid]['lastMove'], 
            accmult=self.users[uid]['accMult'], 
            damagemult=self.users[uid]['damageMult']
        ) # actual move function of the selected move, passing in the level, last move and accuracy and damage multipliers
        
        # {"hit":Bool, "userDamage":int, "enemyDamage":int, "accmult":float, "damagemult":float, "text":str (formatting required)}
        string = moveresult['text'].format(target)

        self.users[uid]['accMult'] = moveresult['accMult'] # apply multipliers
        self.users[uid]['damageMult'] = moveresult['damageMult']
        self.users[uid]['lastMove'] = self.users[uid]['moves'][slot] #set ['lastMove'] to the id of the last move

        await ctx.respond(string)
        if moveresult['hit'] == False:
            return

        try:
            self.users[user]['health'] -= moveresult['enemyDamage']
            self.users[uid]['health'] -= moveresult['userDamage']

        # move code ends here, all below is further boilerplate and near death stuff
        

        except KeyError:
            embed = discord.Embed(
                title='User has no data in JoJoBot'
            )
            await ctx.respond(embed=embed)
            return
        

        if self.users[uid]['health'] < 1 and moveresult['userDamage'] > 0:
            await ctx.send('You died from your own attack. Be careful next time. Welcome back to level zero.')
            self.users = func.reset(uid)

        if self.users[user]['health'] < 1:
            self.users[user]['health'] = 0
            await ctx.send('Your enemy is about to die. Will you kill them (`/kill`) or will you give mercy (`/mercy`)?')
        
        getdata.users.update_info(self.users)

    @commands.slash_command(guild_ids=guilds)
    async def healboth(self, ctx, opponent):
        try:
            if opponent[:2] != '<@':
                await ctx.respond('You must ping a user in `target` section of this command.')
                return
            self.users = getdata.Fetch('./cogs/data/users.json').read_info()

            oppid = opponent[2:len(opponent)-1]

            self.users[oppid]['health'] = self.users[oppid]['maxHealth']
            self.users[oppid]['accMult'] = 1
            self.users[oppid]['damageMult'] = 1

            uid = str(ctx.user.id)
            self.users[uid]['health'] = self.users[uid]['maxHealth']
            self.users[uid]['accMult'] = 1
            self.users[uid]['damageMult'] = 1

            getdata.Fetch('./cogs/data/users.json').update_info(self.users)

            await ctx.respond(f'Healed both <@{ctx.user.id}> and {opponent}. The battlefield levels.')

        except KeyError:
            embed = discord.Embed(
                title='User has no data in JoJoBot'
            )
            await ctx.respond(embed=embed)
            return

    @commands.slash_command(guild_ids=guilds)
    async def kill(self, ctx, target):
        self.users = getdata.Fetch('./cogs/data/users.json').read_info()

        try:
            if target[:2] != '<@':
                await ctx.respond('You must ping a user in `target` section of this command.')
                return
            
            user = target[2:len(target)-1]

            if self.users[user]['health'] != 0:
                await ctx.respond(f"{target}'s health is too high to finish them off.")
                return
            
            self.users[str(ctx.user.id)]['accMult']=1
            self.users[str(ctx.user.id)]['damageMult']=1

            self.users = func.reset(user)

            await ctx.respond(f'You killed {target}. Their stats have been reset to level zero.')
            getdata.users.update_info(self.users)
        except KeyError:
            embed = discord.Embed(
                title='User has no data in JoJoBot'
            )
            await ctx.respond(embed=embed)
            return
        

    @commands.slash_command(guild_ids=guilds)
    async def mercy(self, ctx, target):
        self.users = getdata.Fetch('./cogs/data/users.json').read_info()

        try:
            if target[:2] != '<@':
                await ctx.respond('You must ping a user in `target` section of this command.')
                return
            
            user = target[2:len(target)-1]

            if self.users[user]['health'] != 0:
                await ctx.respond(f"{target}'s health is too high to finish them off.")
                return

            self.users[user]['health'] = self.users[user]['maxHealth']
            self.users[user]['accMult']=1
            self.users[user]['damageMult']=1

            self.users[str(ctx.user.id)]['accMult']=1
            self.users[str(ctx.user.id)]['damageMult']=1

            await ctx.respond(f'You showed mercy to {target}. Their health has been restored.')
            getdata.users.update_info(self.users)

        except KeyError:
            embed = discord.Embed(
                title='User has no data in JoJoBot'
            )
            await ctx.respond(embed=embed)
            return


def setup(client):
    client.add_cog(battle(client))