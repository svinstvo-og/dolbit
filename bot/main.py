import os
import discord
from discord.ext import commands
import youtube_dl
import asyncio
from spoti import *
from yt import *

intents = discord.Intents.default()
intents.message_content = True  # Enable if you want to read message content
intents.voice_states = True  # Enable if you want to detect users in voice channels

song_queue = []


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def join(ctx):
    try:
        if ctx.author.voice:  # Check if the user is in a voice channel
            channel = ctx.author.voice.channel
            await channel.connect()  # Connect to the voice channel
            await ctx.send("Joined the voice channel!")
        else:
            await ctx.send("You need to join a voice channel first!")
    except Exception as e:
        print(f"Error: {e}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Not connected to a voice channel.")

@bot.command()
async def pause(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
    else:
        ctx.voice_client.resume()

@bot.command()
async def resume(ctx):
    if not ctx.voice_client.is_playing():
        ctx.voice_client.resume()

@bot.command()
async def stream(ctx):
    global current_spotify_song

    await ctx.send(f"Streaming music from spotify.")
    while True:
        new_song = get_current_song()

        if new_song is None or new_song == current_spotify_song:
            await asyncio.sleep(1)
            continue

        current_spotify_song = new_song

        await ctx.send(f"Now playing: {current_spotify_song} from Spotify")

        player = await YTDLSource.from_url(current_spotify_song, loop=bot.loop)

        if ctx.voice_client and not ctx.voice_client.is_playing():
            ctx.voice_client.play(player, after=lambda e: print(f'Finished playing: {e}'))
        else:
            ctx.voice_client.stop()
            ctx.voice_client.play(player, after=lambda e: print(f'Finished playing: {e}'))

        await asyncio.sleep(1)

@bot.command()
async def queue(ctx, *, song: str = None):
    if song is None:
        await check(ctx)
    else:
        song_queue.append(song)
        await ctx.send(f"{song} was added to queue.")


@bot.command()
async def check(ctx):
    if len(song_queue) == 0:
        await ctx.send("The queue is empty.")
    else:
        output = "Songs to be played from queue:"
        for i in range(len(song_queue)):
            output += f"\n{i}. {song_queue[i]}"
        await ctx.send(output)

async def play_queue(ctx):
    if len(song_queue) == 0:
        await ctx.send("Queue is empty! Use !queue [name] to add music to queue")
    else:
        song_to_play = song_queue.pop(0)
        player = await YTDLSource.from_url(song_to_play, loop=bot.loop)
        if not ctx.voice_client.is_playing():
            next_song = play_queue(ctx)
            ctx.voice_client.play(player, after = await next_song)

@bot.command()
async def play(ctx, *, search: str = None):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()

        if search is None:
            await play_queue(ctx)

        else:
            await ctx.send(f"Playing {search}")
            player = await YTDLSource.from_url(search, loop=bot.loop)
            ctx.voice_client.play(player)
    else:
        await ctx.send("You need to be in a voice channel to play music.")

@bot.command()
async def skip(ctx):
    if len(song_queue) == 1:
        ctx.voice_client.pause()
    if len(song_queue) >= 2:
        ctx.voice_client.stop()
        await play(ctx)

@bot.command()
async def clear(ctx):
    ...

bot.run("MTI4NDkxNzQ4MDczNjk0ODI1NQ.GSJiJm.AyXIhRcMEtDeRRprXys5PM6_9YNzCVb4QrTpts")