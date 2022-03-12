import discord
from discord.ext import commands
import os
import youtube_dl
import time

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.is_playing = False
        self.music_queue = []
        self.vc = ''
        self.ctx = ''
        self.in_loop = False
        self.FFMPEG_OPTIONS = {
        'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cargado con éxito\n-----")

    def next(self):
        if len(self.music_queue) > 0:
            if self.in_loop == False:
                self.music_queue.pop(0)
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0]['source']
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda x: self.next())
        else:
            self.is_playing = False

    @commands.command(name="disconnect",
    aliases=["dis", "leave"],
    description="Desconecta al bot del canal de voz")
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Desconectado 📴")

    @commands.command(name="play", aliases=["p"], description="Reproduce canciones")
    async def play(self, ctx, *, music):
        if music == None:
            await ctx.send("Tienes que poner el nombre o el link de alguna canción")
        else:
            if ctx.author.voice is None:
                await ctx.send("No estás en ningún canal")
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)
            YDL_OPTIONS = {'format': "bestaudio"}
            self.vc = ctx.voice_client

            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                if music.startswith("https://www.youtube.com")or music.startswith("https://youtu.be"):
                    info = ydl.extract_info(music , download=False)
                else:
                    info = ydl.extract_info("ytsearch:%s" %music , download=False)['entries'][0]

                if info['duration'] >= 3600:
                    duration = time.strftime("%H:%M:%S", time.gmtime(info['duration']))
                else:
                    duration = time.strftime("%M:%S", time.gmtime(info['duration']))
                self.music_queue.append({'source': info['formats'][0]['url'], 'title': info['title'], 'duration': duration})
            if self.is_playing == False:
                self.is_playing = True
                m_url = self.music_queue[0]['source']
                title = self.music_queue[0]['title']
                duration = self.music_queue[0]['duration']
                source = await discord.FFmpegOpusAudio.from_probe(m_url, **self.FFMPEG_OPTIONS)
                self.vc.play(source, after=lambda x: self.next())
                await ctx.send('▶️ Reproduciendo...\n' + '**' + title + '** | (`' + duration + '`)')
            else:
                title = info['title']
                await ctx.send('**' + title + '** | (`' + duration + '`) añadido a la cola')

    @commands.command(name="pause", aliases=["ps"], description="Pausa la canción")
    async def pause(self, ctx):
        if self.vc and self.vc.is_playing():
            self.vc.pause()
            if self.vc and self.vc.is_paused():
                await ctx.send('Pausado ⏸️')
        else:
            await ctx.send('No hay ninguna canción en reproducción')

    @commands.command(name="resume", aliases=["rs"], description="Continua con la reproducción de la canción")
    async def resume(self, ctx):
        if self.vc and self.vc.is_paused():
            self.vc.resume()
            if self.vc and self.vc.is_playing():
                await ctx.send('Reanudado ⏯️')
        else:
            await ctx.send('No hay ninguna canción pausada')

    @commands.command(name="stop", description="Detiene la  reproducción de todas las canciones")
    async def stop(self, ctx):
        if self.vc.is_playing() or self.vc.is_paused:
            self.music_queue = []
            self.vc.stop()
            await ctx.send('Detenido ⏹️')
        else:
            await ctx.send('No estoy en reproducción')

    @commands.command(name="skip", aliases=['s'],  description="Salta a la siguiente canción en la cola")
    async def skip(self, ctx):
        if self.is_playing:
            self.vc.stop()
            if len(self.music_queue)>0:
                await ctx.send('Siguiente ⏭️️')
                if len(self.music_queue)>0:
                    title = self.music_queue[0]['title']
                    duration = self.music_queue[0]['duration']
                    await ctx.send('▶️ Reproduciendo...\n' + '**' + title + '** | (`' + duration + '`)')
                else:
                    await ctx.send('No hay nada más en cola')
            else:
                await ctx.send('No hay nada más en cola')
        else:
            await ctx.send('No hay nada en reproducción')

    @commands.command(name="queue", aliases=["q"], description="Muestra la cola de reproducción")
    async def q(self, ctx):
        cola = ""
        for i in range(1, len(self.music_queue)):
            cola += str(i) + '.- ' + self.music_queue[i]['title'] + "\n"

        if cola != "":
            qembed = discord.Embed(
            title=f"Cola de reproducción",
            colour=discord.Color.orange(),
            description=cola,
            timestamp=ctx.message.created_at,
            )
            title = self.music_queue[0]['title']
            duration = self.music_queue[0]['duration']
            await ctx.send('▶️ Reproduciendo...\n' + '**' + title + '** | (`' + duration + '`)', embed=qembed)
        else:
            if self.is_playing:
                qembed = discord.Embed(
                title=f"Cola de reproducción",
                colour=discord.Color.orange(),
                description='Cola vacía',
                timestamp=ctx.message.created_at,
                )
                title = self.music_queue[0]['title']
                duration = self.music_queue[0]['duration']
                await ctx.send('▶️ Reproduciendo...\n' + '**' + title + '** | (`' + duration + '`)', embed=qembed)
            else:
                await ctx.send('No estoy en reproducción')
    
    @commands.command(name="loop", description="Pone en bucle la canción en reproducción actual")
    async def loop(self, ctx):
        if self.is_playing:
            if self.in_loop == False:
                self.in_loop = True
                await ctx.send('**🔂Bucle:** *Activado*')
            else:
                self.in_loop = False
                await ctx.send('**🔂Bucle:** *Desactivado*')
        else:
            await ctx.send('No estoy en reproducción')

def setup(client):
    client.add_cog(Music(client))
