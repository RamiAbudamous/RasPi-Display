import os
from time import sleep
from pynput.mouse import Listener, Button

from scripts import athan
import datetime
from datetime import datetime

from scripts import spotifyTrackInfo
from scripts import calc

# GLOBALS
state=0
currState=0
# Athan Globals
locState=0 #location state
currLocState=0 #current location state that gets changed
maxLocs=0
names = []
lats = []
longs = []
prayerID = {0: "Fajr", 1: "Sunrise", 2: "Duhr", 3: "Asr", 4: "Maghrib", 5: "Isha"}
# Spotify Globals
playState=0
currPlayState=0

# Define States
MAX_STATES=1
ATHAN = 0
SPOTIFY = 1
CALC = 2

#State Management
def on_click(x, y, button, pressed):
    global currState
    if pressed:
        if button==Button.right:
            # print("click right")
            currState+=1
            if currState>MAX_STATES:
                currState=0
        elif button==Button.left:
            # print("click left")
            currState-=1
            if currState<0:
                currState=MAX_STATES

def on_scroll(x, y, dx, dy):
    global currLocState
    if dy>0:
        # print("scroll up")
        currLocState+=1
        if currLocState>maxLocs:
            currLocState=0
    elif dy<0:
        # print("scroll down")
        currLocState-=1
        if currLocState<0:
            currLocState=maxLocs

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
    maxLocs-=1 #0 index
    
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
        current_track = spotifyTrackInfo.getCurrentTrack()
        os.system('cls')
        spotifyTrackInfo.printSongInfo(current_track)
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