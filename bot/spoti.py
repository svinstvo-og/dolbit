import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='e37fc1aaa8674c698db49f179632fd50',
                                               client_secret='7a9431b41eff4f809e592b6b248aa948',
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='user-read-playback-state'))

current_spotify_song = None

def get_current_song():
    current_playback = sp.current_playback()
    if current_playback is not None and current_playback['is_playing']:
        return f"{current_playback['item']['name']}, {current_playback['item']['artists'][0]['name']}"
    else:
        return None
    
#print(get_current_song())