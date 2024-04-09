#THIS PROGRAM USES PYCORD, NOT DISCORD.PY BECAUSE IT IS BOILERPLATE CITY

import discord #pycord
from discord.ext import commands
import json
import os
import cogs.getdata
import math
import cogs.func as func

intents = discord.Intents.default()
intents.messages = True

guilds = [
    690194500039082053,
    940890627221110795,
    939710720227041290
]

amntActStands = 3

with open('./token.json', 'r') as file:
    token = json.load(file)['token']

client = commands.Bot(command_prefix='!!', intents=intents)

exclude = ['getdata.py', 'func.py']

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and (filename not in exclude):
        client.load_extension(f"cogs.{filename[:-3]}")
        print('imported', filename[:-3])

@client.event
async def on_ready():

        #await client.sync_commands()

    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.bot:
        return

    try:
        users = cogs.getdata.users.read_info()
        stands = cogs.getdata.Fetch('./cogs/data/standlist.json').read_info()
        users[str(message.author.id)]
        id = str(message.author.id)
        users[id]['exp'] += 1
        if users[id]['exp'] == users[id]['reqExp']:
            users[id]['level'] += 1
            users[id]['reqExp'] = math.floor((users[id]['level']+4) ** 2)
            #users[id]['exp'] = 0
            users[id]['health'] = math.ceil(users[id]['health'] * 1.02)
            users[id]['maxHealth'] = math.ceil(users[id]['maxHealth'] * 1.02)
            print(message.author.name, 'reached level', users[id]['level'])
            embed = discord.Embed(
                title=f'You reached level {users[id]["level"]}',
                description='You may have unlocked new moves. Use `/viewmoves` to view your available moves.',
                color=discord.Colour.teal()
            )
            await message.channel.send(embed=embed)

            standid = str(users[id]['stand'])
            if len(stands[standid]['acts']) > 1 and stands[standid]['acts'][len(stands[standid]['acts'])-1] == users[id]['level']:
                users[id]['stand'] += 0.1
                await message.channel.send(embed=discord.Embed(
                    title=f'You unlocked {stands[str(users[id]["stand"])]["name"]}',
                    color = discord.Colour.teal()
                ))
                print('     They unlocked', stands[str(users[id]["stand"])]["name"])

        cogs.getdata.users.update_info(users)

    except:
        users = func.reset(str(message.author.id))
        cogs.getdata.users.update_info(users)
        print('initialised user', message.author.name)

    await client.process_commands(message)

def isOwner(id):
    if id == 589489342234492928: #my id
        return True
    else:
        return False

@client.slash_command()
async def test(ctx):
    if isOwner(ctx.user.id):
        print('test')
        await ctx.respond('test')
        await ctx.respond(f'server id: {ctx.guild_id}')
    else:
        await ctx.respond(f'You cannot do this command unless you are the owner of this bot.')

@client.slash_command(guild_ids=guilds)
async def do(ctx, command):
    if isOwner(ctx.user.id):
        print('do')
        await ctx.respond('sending message...')
        await ctx.send(command)
    else:
        await ctx.respond(f'You cannot do this command unless you are the owner of this bot.')

@client.slash_command(guild_ids=guilds)
async def unload_module(ctx, module):
    if isOwner(ctx.user.id):
        await ctx.respond(f'unloading module {module}')
        client.unload_extension(f"cogs.{module}")
        print('unloaded module', module)
    else:
        await ctx.respond(f'You cannot do this command unless you are the owner of this bot.')

@client.slash_command(guild_ids=guilds)
async def load_module(ctx, module):
    if isOwner(ctx.user.id):
        await ctx.respond(f'loading module {module}')
        client.load_extension(f'cogs.{module}')
        print('loaded module', module)
    else:
        await ctx.respond(f'You cannot do this command unless you are the owner of this bot.')

@client.slash_command(guild_ids=guilds)
async def sync_modules(ctx):
    if isOwner(ctx.user.id):
        await ctx.respond('syncing')
        await client.sync_commands()
        print('module syncing')
    else:
        await ctx.respond(f'You cannot do this command unless you are the owner of this bot.')


client.run(token)
