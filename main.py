import discord
from discord.ext import commands
import os
from pathlib import Path

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(cwd + """
-----""")

client = commands.Bot(command_prefix = 'p!') #prefix del bot
client.version = '0.3'

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Expandir el Tahuantinsuyo', emoji=None))
    print('Se me prendio el bot')

@client.command(name='ping')
async def ping (ctx):
    embed=discord.Embed(title="Pong!🏓", description=f'Tengo {round(client.latency*1000)}ms de ping', colour=discord.Colour.orange())
    await ctx.send(embed=embed)

client.remove_command('help')

if __name__ == "__main__":
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")
    
    client.run(os.environ['token'])
