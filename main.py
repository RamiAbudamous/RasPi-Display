import os
from time import sleep
from pynput.mouse import Listener, Button

from scripts import system

from scripts import athan
import datetime
from datetime import datetime

from scripts import spotifyTrackInfo
from scripts import calc

# Define States
MAX_STATES = 2
SYSTEM = 0
ATHAN = 1
SPOTIFY = 2
CALC = 3

# System sunstates
OVERVIEW = 0
CPU = 1
MEMORY = 2
DISK = 3
NETWORK = 4

# Spotify substates
MAX_SPOTIFY_STATES = 1
SONG_INFO = 0
CURR_QUEUE = 1

# GLOBALS
state=0
currState=0
# System Globals
MAX_SYSTEM_STATES = 4
sysState = 0
currSysState = 0
# Athan Globals
maxLocs=-1 #maximum locations, starts as -1 for 0 index.
locState=0 #location state
currLocState=0 #current location state that gets changed
names = []
lats = []
longs = []
# Spotify Globals
playState=0
currPlayState=0
spotifyImage=""


#State Management
def incState(incdState, max):
    incdState+=1
    if incdState>max:
        incdState=0
    return incdState

def decState(decdState, max):
    decdState-=1
    if decdState<0:
        decdState=max
    return decdState

def on_click(x, y, button, pressed):
    global currState
    if pressed:
        if button==Button.left:
            currState = incState(currState, MAX_STATES)
        elif button==Button.right:
            # print("click right")
            currState = decState(currState, MAX_STATES)

def on_scroll(x, y, dx, dy):
    global currSysState, currLocState, currPlayState
    if dy>0:
        # print("scroll up")
        currSysState = incState(currSysState, MAX_SYSTEM_STATES)
        currLocState = incState(currLocState, maxLocs)
        currPlayState = incState(currPlayState, MAX_SPOTIFY_STATES)
    elif dy<0:
        # print("scroll down")
        currSysState = decState(currSysState, MAX_SYSTEM_STATES)
        currLocState = decState(currLocState, maxLocs)
        currPlayState = decState(currPlayState, MAX_SPOTIFY_STATES)

# STATES
def systemState():
    while(state==currState):
        sysState = currSysState
        while((state==currState) and (sysState==currSysState)):
            
            if sysState==OVERVIEW:
                system.getStats()
            elif sysState==CPU:
                system.getCPUStats()
            elif sysState==MEMORY:
                system.getMemStats()
            elif sysState==DISK:
                system.getDiskStats()
            elif sysState==NETWORK:
                system.getNetStats()

            sleep(.99)

def athanState():
    global maxLocs, locState, currState
    
    with open('data/locations.txt', 'r') as location_file:
        locations = location_file.readlines()
        if len(locations)%3!=0:
            print("Invalid number of lines.")
        for i in range(int(len(locations)/3)):
            idx = i*3
            names.append(locations[idx].strip())
            lats.append(locations[idx+1].strip())
            longs.append(locations[idx+2].strip())
            maxLocs+=1
    
    while(state==currState):
        locState = currLocState
        now = datetime.now()

        startDate = now.day

        data = athan.callAthanAPI(now, lats[locState], longs[locState])
        timings = data["data"]["timings"]
        prayerTimes = athan.getTimings(timings)

        #initial currTime
        currDate = now.day

        while((currDate==startDate) and (state==currState) and (locState==currLocState)):
            currTime = datetime.now()
            currDate = currTime.date
            athan.outputAthan(prayerTimes, names[locState], currTime)


def spotifyState():
    while(state==currState):
        global spotifyImage
        playState = currPlayState

        #call api for info
        spotifyCreds = spotifyTrackInfo.getSpotifyCreds()
        # queue = spotifyTrackInfo.getSpotifyQueue(spotifyTrackInfo.getSpotifyCreds())
        # once you have the queue, you can get the current track from there too.
        while((state==currState) and (playState==currPlayState)):
            if playState==SONG_INFO:
                # maybe have both calls happen ebfore the update. queue displays how far youre into the song
                current_track = spotifyTrackInfo.getSpotifyTrack(spotifyCreds)
                os.system('cls')
                newSpotifyImage = spotifyTrackInfo.printSongInfo(current_track) #and queue, or maybe only queue
                if newSpotifyImage!=spotifyImage:
                    spotifyImage = newSpotifyImage
                    spotifyTrackInfo.displayImg(spotifyImage)
                sleep(.99)

            elif playState==CURR_QUEUE:
                os.system('cls')
                # spotifyTrackInfo.printQueueInfo(queue)
                print(f"in queue")
                sleep(.99)

def calcState():
    print("in calc state")


def mainState():
    global state, currState
    # initial values
    currState = 0

    while(1): #runs forever
        state=currState

        # print(f"in state selector, state={state}, currstate={currState}, maxstates={MAX_STATES}")
        if state==SYSTEM:
            systemState()
        elif state==ATHAN:
            athanState()
        elif state==SPOTIFY:
            spotifyState()
        elif state==CALC:
            calcState()
        else:
            print("INVALID STATE")
            exit(1)
        # print(f"end of state selector, state={state}, currstate={currState}\n\n")
        # sleep(1)

if __name__ == "__main__":
    # on scroll, change state
    listener = Listener(on_click=on_click, on_scroll=on_scroll)
    listener.start()

    mainState()