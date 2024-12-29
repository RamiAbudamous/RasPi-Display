import os
from time import sleep
from pynput.mouse import Listener, Button

from scripts import athan
import datetime
from datetime import datetime

from scripts import spotifyTrackInfo
from scripts import calc

# Define States
MAX_STATES=1
ATHAN = 0
SPOTIFY = 1
CALC = 2

# Spotify substates
MAX_SPOTIFY_STATES = 1
SONG_INFO = 0
CURR_QUEUE = 1

# GLOBALS
state=0
currState=0
# Athan Globals
maxLocs=-1 #maximum locations, starts as -1 for 0 index.
locState=0 #location state
currLocState=0 #current location state that gets changed
names = []
lats = []
longs = []
prayerID = {0: "Fajr", 1: "Sunrise", 2: "Duhr", 3: "Asr", 4: "Maghrib", 5: "Isha"}
# Spotify Globals
playState=0
currPlayState=0


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
        if button==Button.right:
            currState = incState(currState, MAX_STATES)
        elif button==Button.left:
            # print("click left")
            currState = decState(currState, MAX_STATES)

def on_scroll(x, y, dx, dy):
    global currLocState, currPlayState
    if dy>0:
        # print("scroll up")
        currLocState = incState(currLocState, maxLocs)
        currPlayState = incState(currPlayState, MAX_SPOTIFY_STATES)
    elif dy<0:
        # print("scroll down")
        currLocState = decState(currLocState, maxLocs)
        currPlayState = decState(currPlayState, MAX_SPOTIFY_STATES)

# STATES
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
        startTime = f"{now.hour}:{now.minute}"
        startTimeInt = athan.timeToMins(startTime)

        data = athan.callAthanAPI(now, lats[locState], longs[locState])
        timings = data["data"]["timings"]
        prayerTimes = athan.getTimings(timings)

        #initial currTime
        currDate = now.day
        currTime = f"{now.hour}:{now.minute}"
        currTimeInt = athan.timeToMins(currTime)

        while((currDate==startDate) and (state==currState) and (locState==currLocState)):
            #update currTime
            nowNow = datetime.now()
            currDate = nowNow.day
            currTime = f"{nowNow.hour}:{nowNow.minute}"
            currTimeInt = athan.timeToMins(currTime)
            currTime = f"{athan.minsToTime(athan.timeToMins(currTime))}:{str(nowNow.second).zfill(2)}" #mins to time then time to mins is the easiest way to convert from 24 to 12 hour
            
            # check if the next prayer time is here
            nextPrayer = None
            for i in range(len(prayerTimes)):
                if prayerTimes[i]>currTimeInt:
                    nextPrayer = prayerTimes[i]
                    nextPrayerName = prayerID.get(i)
                    break

            os.system('cls')
            # now that everything is calculated, print them all
            print(f"     {currTime}")
            print(f"{nowNow.month}/{nowNow.day}/{nowNow.year}, {names[locState]}")
            #print timings as time
            print(f"Fajr        {athan.minsToTime(prayerTimes[0])}")
            print(f"Sunrise     {athan.minsToTime(prayerTimes[1])}")
            print(f"Duhr        {athan.minsToTime(prayerTimes[2])}")
            print(f"Asr         {athan.minsToTime(prayerTimes[3])}")
            print(f"Maghrib     {athan.minsToTime(prayerTimes[4])}")
            print(f"Isha        {athan.minsToTime(prayerTimes[5])}")

            if nextPrayer!=None:
                timeToNext = nextPrayer-currTimeInt
                hoursToNext = int(timeToNext/60)
                minsToNext = int(timeToNext%60)
                if hoursToNext!=0:
                    print(f"{nextPrayerName} in {hoursToNext} hours and {minsToNext} minutes")
                else: print(f"{nextPrayerName} in {minsToNext} minutes")
            else: print("All Prayers Complete!")

            sleep(.99) #wait until the next second
            #.99 because each iteration of this loop takes roughly .005 seconds


def spotifyState():
    while(state==currState):
        playState = currPlayState

        #call api for info
        spotifyCreds = spotifyTrackInfo.getSpotifyCreds()
        current_track = spotifyTrackInfo.getSpotifyTrack(spotifyCreds)
        # queue = spotifyTrackInfo.getSpotifyQueue(spotifyTrackInfo.getSpotifyCreds())
        # once you have the queue, you can get the current track from there too.
        while((state==currState) and (playState==currPlayState)):
            if playState==SONG_INFO:
                # maybe have both calls happen ebfore the update. queue displays how far youre into the song
                os.system('cls')
                spotifyTrackInfo.printSongInfo(current_track) #and queue, or maybe only queue
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
        if state==ATHAN:
            athanState()
        elif state==SPOTIFY:
            spotifyState()
        elif state==CALC:
            calcState
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