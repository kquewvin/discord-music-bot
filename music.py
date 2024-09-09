import discord
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv

# Add queue system
# Add searchable youtube videos with python requests

def run_bot():
    load_dotenv()
    TOKEN = os.getenv("discord_token")
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    voice_clients = {}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    ffmpeg_options = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn -filter:a 'volume=0.25'"}

    @client.event
    async def on_ready():
        print(f"{client.user} is now listening!")
    
    @client.event
    async def on_message(message):
        if message.content.startswith("?play"):
            if message.author.voice is None:
                await message.channel.send("You need to be in a voice channel to play music")

            try:
                voice_client = await message.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except Exception as e:
                print(e)

            try:
                url = message.content.split()[1]

                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                song = data["url"]
                player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

                voice_clients[message.guild.id].play(player)

                await message.channel.send(f"Now playing: {data['title']}")
            except Exception as e:
                print(f"Error: {e}")
                await message.channel.send("An error occured while trying to play the song")

    client.run(TOKEN)