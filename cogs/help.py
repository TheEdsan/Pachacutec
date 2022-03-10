import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cargado con éxito\n-----")

    @commands.command(
        name="help", aliases=['h', 'commands', 'cmds'], description="Lista de comandos"
    )
    async def help(self, ctx, cmd = None):
      if cmd is None :
        helpEmbed = discord.Embed(title = "Lista de comandos", colour= discord.Color.orange(), timestamp=ctx.message.created_at,)
        helpEmbed.add_field(name="Música",
        value="""**p!play** - *Reproduce canciones*
        **p!pause** - *Pausa la canción*
        **p!resume** - *Continua con la reproducción de la canción*
        **p!skip** - *Salta a la siguiente canción en la cola*
        **p!stop** - *Detiene la  reproducción de todas las canciones*
        **p!queue** - *Muestra la cola de reproducción*
        **p!loop** - *Pone en bucle la canción en reproducción actual*
        **p!disconnect** - *Desconecta al bot del canal de voz*""", inline=False)
        helpEmbed.add_field(name="Extra", value="**p!ping** - *Muestra la latencia del bot*")
        helpEmbed.add_field(name="Bot", value="**p!bot** - *Información del bot*")
      else:
        pass
      await ctx.send(embed = helpEmbed)

def setup(client):
    client.add_cog(Help(client))