import discord
from discord.ext import commands

guilds = [
    690194500039082053,
    940890627221110795,
    939710720227041290
]

class testing(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(guild_ids=guilds)
    async def testrep(self, ctx):
        print('testrep')
        await ctx.respond('testing, testing, 1, 2, 3')

def setup(client):
    client.add_cog(testing(client))
