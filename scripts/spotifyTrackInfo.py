import spotipy
# import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import urllib.request
from PIL import Image

def calcProgressBar(progress, duration, segments=10):
    percentage = progress/duration
    filledSegments = int(percentage*segments)
    bar = "█" * filledSegments + "-" * (segments-filledSegments)
    return f"[{bar}]"

def centerOutput(lines):
    max_length = max(len(line) for line in lines)
    #add padding to center lines
    centered_lines = [line.center(max_length) for line in lines]
    return "\n".join(centered_lines)

def getSpotifyCreds():
    with open('data/client.txt', 'r') as client_file:
        clients = client_file.readlines()
        clientID = clients[0].strip()
        clientSec = clients[1].strip()
        redirectUri = clients[2].strip()
        username = clients[3].strip()

    #only need the first
    scope = 'user-read-playback-state user-read-currently-playing user-modify-playback-state'
    # scope = 'user-modify-playback-state'

    # token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSec, redirect_uri=redirectUri)
    # spotify = spotipy.Spotify(auth=token)
    spotifyCreds = spotipy.Spotify(auth_manager=SpotifyOAuth(username=username, scope=scope, client_id=clientID, client_secret=clientSec, redirect_uri=redirectUri))
    return spotifyCreds

def getSpotifyTrack(sp):
    return sp.current_user_playing_track()

def getSpotifyQueue(sp):
    return sp.queue()

def displayImg(imageURL):
    urllib.request.urlretrieve(imageURL, "image.png")
    img = Image.open(r"image.png")
    img.show()

def printSongInfo(current_track):
    if current_track!=None:
        # data = json.loads(str(current_track))
        song = current_track["item"] #json of data. not the song name.
        
        # get currently playing from queue
        # song = current_track["currently_playing"] #json of data. not the song name.
        
        playing = current_track["is_playing"]
        progress_ms = current_track["progress_ms"]
        duration_ms = song["duration_ms"]


        album = song["album"]["name"]
        art = song["album"]["images"][1]["url"]

        # print("300x300")
        # print(song["album"]["images"][1])
        # print("64x64")
        # print(song["album"]["images"][2])
        # exit(0)
        
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

        progress = int(progress_ms/1000)
        duration = int(duration_ms/1000)

        bar = calcProgressBar(progress, duration)

        progress_min = f"{int(progress/60)}:{str(progress%60).zfill(2)}"
        duration_min = f"{int(duration/60)}:{str(duration%60).zfill(2)}"

        playEmoji = "❚❚"
        if (playing==False): playEmoji = "▶"

        lines = [songName, artistList, album, playEmoji, f"{progress_min} {bar} {duration_min}"]
        # print(f"{songName}\n{artistList}\n{album}\n{progress_min} {bar} {duration_min}\n\n{art}")
        print(centerOutput(lines))
        # print(f"\n\nImage link:\n{art}")
    else: print("Not playing a song.")

    return art