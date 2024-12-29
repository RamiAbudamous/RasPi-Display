import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth

with open('client.txt', 'r') as client_file:
    clients = client_file.readlines()
    clientID = clients[0].strip()
    clientSec = clients[1].strip()
    redirectUri = clients[2].strip()
    username = clients[3].strip()

#only need the first
scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'

# token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSec, redirect_uri=redirectUri)
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(username=username, scope=scope, client_id=clientID, client_secret=clientSec, redirect_uri=redirectUri))
# spotify = spotipy.Spotify(auth=token)
current_track = spotify.current_user_playing_track()

# print(f"current track info:\n\n\n\n\n")

if current_track!=None:
    # data = json.loads(str(current_track))
    song = current_track["item"] #json of data. not the song name.

    album = song["album"]["name"]
    art = song["album"]["images"][0]["url"] #might be [0][url]
    songName = song["name"]

    artists = []
    for artist in song["artists"]:
        artists.append(artist["name"])

    artistList = ""
    if len(artists)==1:
        artistList = artists[0]
    elif len(artists)>1:
        for i in range(len(artists)-1):
            artistList += f"{artists[i]}, "
        artistList += f"{artists[len(artists)-1]}"

    print(f"{songName}\n{artistList}\n{album}\n{art}")
else: print("Not playing a song.")