import platform

import discord
from discord.ext import commands

class Bot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cargado con éxito\n-----")

    @commands.command(
        name="bot", description="Información del Bot"
    )
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))
        prefix = "pb!"

        embed = discord.Embed(
            title=f"Mi Información",
            colour=discord.Color.orange(),
            timestamp=ctx.message.created_at,
        )

        embed.add_field(name="Mi prefijo:", value=prefix)
        embed.add_field(name="Mi Versión:", value=self.client.version)
        embed.add_field(name="Versión de Python:", value=pythonVersion)
        embed.add_field(name="Versión de Discord.Py", value=dpyVersion)
        embed.add_field(name="Total de servidores:", value=serverCount)
        embed.add_field(name="Total de usuarios:", value=memberCount)
        embed.add_field(name="Mi desarrollador:", value="<@723743005093134408>")

        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Bot(client))
