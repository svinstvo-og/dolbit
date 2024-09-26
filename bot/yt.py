import yt_dlp as youtube_dl
import asyncio
import discord
from spoti import *

ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',  # Avoid downloading entire playlists
    'quiet': True,  # Suppress unnecessary output
    'no_warnings': True,
    'default_search': 'auto',
    'extractaudio': True,  # Extract only audio
    'audioformat': 'mp3',  # Optional: specify format
    'nocheckcertificate': True,
    'source_address': '0.0.0.0',
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

def search_youtube(query):
    with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            return info['formats'][0]['url']
        except Exception as e:
            print(f"Error: {e}")
            return None
        

'''def test():
    song, artist = get_current_song()
    if song and artist:
        query = f"{song} {artist}"
        youtube_url = search_youtube(query)
    return youtube_url

test()'''