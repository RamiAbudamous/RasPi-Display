# Screen imports
import board
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import adafruit_ili9341
from fourwire import FourWire
from datetime import datetime
from time import sleep
import calendar

# Other imports
import os
import requests
import json

# Screen info defined here
display = 0
WIDTH = 240
HEIGHT = 320
ROT = 90
BACKGROUND_COLOR = 0x2ABCDE
TEXT_COLOR = 0xF7EE0B

prayerID = {0: "Fajr", 1: "Sunrise", 2: "Duhr", 3: "Asr", 4: "Maghrib", 5: "Isha"}
PRAYER_TEXT_SCALE = 2

maxLocs=-1 #maximum locations, starts as -1 for 0 index.
locState=0 #location state
currLocState=0 #current location state that gets changed
names = []
lats = []
longs = []

#Athan Funcs
def callAthanAPI(currTime, lat, long):
    #method 2 is North America Islamic Association's method for deciding athan time
    url = f"https://api.aladhan.com/v1/timings/{currTime.day}-{currTime.month}-{currTime.year}"
    querystring = {"latitude":f"{lat}", "longitude":f"{long}", "method":"2"}
    response = requests.request("GET", url, params=querystring)
    return json.loads(response.text)

def getTimings(timings):
    #get timings as int minutes
    fajr = timeToMins(timings["Fajr"])
    sunrise = timeToMins(timings["Sunrise"])
    duhr = timeToMins(timings["Dhuhr"])
    asr = timeToMins(timings["Asr"])
    maghrib = timeToMins(timings["Maghrib"])
    isha = timeToMins(timings["Isha"])
    return [fajr, sunrise, duhr, asr, maghrib, isha]

def timeToMins(time):
    hours, minutes = map(int, time.split(':'))
    return (hours*60)+minutes

def minsToTime(time):
    hours = int(time/60)
    if hours>12: hours-=12 # convert 24 hour time to 12, ex: 14 becomes 2
    if hours==0: hours=12 # midnight is 12 not 0
    mins = time%60
    return f"{hours:2}:{str(mins).zfill(2)}"


def outputAthan(prayerTimes, locationName, nowNow):

    # background
    bitmap = displayio.Bitmap(WIDTH-1, HEIGHT-1, 1)
    palette = displayio.Palette(1)
    palette[0] = BACKGROUND_COLOR

    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    mainGroup = displayio.Group()
    mainGroup.append(tile_grid)
    display.root_group = mainGroup

    currTime = f"{nowNow.hour}:{nowNow.minute}"
    currTimeInt = timeToMins(currTime)
    currTime = f"{minsToTime(timeToMins(currTime))}:{str(nowNow.second).zfill(2)}" #mins to time then time to mins is the easiest way to convert from 24 to 12 hour
    
    # check if the next prayer time is here
    nextPrayer = None
    for i in range(len(prayerTimes)):
        if prayerTimes[i]>currTimeInt:
            nextPrayer = prayerTimes[i]
            nextPrayerName = prayerID.get(i)
            break

    # create time label
    font = terminalio.FONT
    # font = bitmap_font.load_font("bdf/icl8x8u.bdf")
    # font = bitmap_font.load_font("fonts/Chroma48Medium-8.bdf")
    # font = bitmap_font.load_font("fonts/Junction-regular-24.bdf")
    # font = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf")
    timeLabel = label.Label(font, text=currTime, color=TEXT_COLOR, scale=3)
    timeLabel.anchor_point = (.5, 0)
    timeLabel.anchored_position = ((WIDTH-1)/2, (HEIGHT-1)/10)
    timeLabel.padding_left = 24 #padding so that the text doesnt overlap on itself. might have to replace with a background
    timeLabel.padding_right = 24
    mainGroup.append(timeLabel)

    # date label
    # currDate = f"{calendar.month_name[nowNow.month]} {nowNow.day}, {nowNow.year} | {locationName}"
    # too long for the display lmao
    currDate = f"{nowNow.month}/{nowNow.day}/{nowNow.year} - {locationName}"
    dateLabel = label.Label(font, text=currDate, color=TEXT_COLOR, scale=2)
    dateLabel.anchor_point = (.5, 0)
    dateLabel.anchored_position = ((WIDTH-1)/2, ((HEIGHT-1)/8)+((HEIGHT-1)/8))
    mainGroup.append(dateLabel)

    fajrText =    f"Fajr        {minsToTime(prayerTimes[0])}"
    sunriseText = f"Sunrise     {minsToTime(prayerTimes[1])}"
    duhrText =    f"Duhr        {minsToTime(prayerTimes[2])}"
    asrText =     f"Asr         {minsToTime(prayerTimes[3])}"
    maghribText = f"Maghrib     {minsToTime(prayerTimes[4])}"
    ishaText =    f"Isha        {minsToTime(prayerTimes[5])}"

    # prayer labels
    fajrLabel = label.Label(font, text=fajrText, color=TEXT_COLOR, scale=PRAYER_TEXT_SCALE)
    fajrLabel.anchor_point = (0, 0)
    fajrLabel.anchored_position = (16, 120)
    mainGroup.append(fajrLabel)
    
    sunriseLabel = label.Label(font, text=sunriseText, color=TEXT_COLOR, scale=PRAYER_TEXT_SCALE)
    sunriseLabel.anchor_point = (0, 0)
    sunriseLabel.anchored_position = (16, 120 + (12*PRAYER_TEXT_SCALE*1))
    mainGroup.append(sunriseLabel)
    
    duhrLabel = label.Label(font, text=duhrText, color=TEXT_COLOR, scale=PRAYER_TEXT_SCALE)
    duhrLabel.anchor_point = (0, 0)
    duhrLabel.anchored_position = (16, 120 + (12*PRAYER_TEXT_SCALE*2))
    mainGroup.append(duhrLabel)
    
    asrLabel = label.Label(font, text=asrText, color=TEXT_COLOR, scale=PRAYER_TEXT_SCALE)
    asrLabel.anchor_point = (0, 0)
    asrLabel.anchored_position = (16, 120 + (12*PRAYER_TEXT_SCALE*3))
    mainGroup.append(asrLabel)
    
    maghribLabel = label.Label(font, text=maghribText, color=TEXT_COLOR, scale=PRAYER_TEXT_SCALE)
    maghribLabel.anchor_point = (0, 0)
    maghribLabel.anchored_position = (16, 120 + (12*PRAYER_TEXT_SCALE*4))
    mainGroup.append(maghribLabel)
    
    ishaLabel = label.Label(font, text=ishaText, color=TEXT_COLOR, scale=PRAYER_TEXT_SCALE)
    ishaLabel.anchor_point = (0, 0)
    ishaLabel.anchored_position = (16, 120 + (12*PRAYER_TEXT_SCALE*5))
    mainGroup.append(ishaLabel)

    if nextPrayer!=None:
        timeToNext = nextPrayer-currTimeInt
        hoursToNext = int(timeToNext/60)
        minsToNext = int(timeToNext%60)
        if hoursToNext!=0:
            nextText = f"{nextPrayerName} in {hoursToNext} hours and {minsToNext} mins"
        else: nextText = f"{nextPrayerName} in {minsToNext} mins"
    else: nextText = "All Prayers Done!"

    nextLabel = label.Label(font, text=nextText, color=TEXT_COLOR, scale=PRAYER_TEXT_SCALE)
    nextLabel.anchor_point = (.5, 0)
    nextLabel.anchored_position = ((WIDTH-1)/2, 128 + (12*PRAYER_TEXT_SCALE*6))
    mainGroup.append(nextLabel)

    # os.system('clear')
    # # now that everything is calculated, print them all
    # print(f"     {currTime}")
    # print(f"{nowNow.month}/{nowNow.day}/{nowNow.year}, {locationName}")
    # #print timings as time
    # print(f"Fajr        {minsToTime(prayerTimes[0])}")
    # print(f"Sunrise     {minsToTime(prayerTimes[1])}")
    # print(f"Duhr        {minsToTime(prayerTimes[2])}")
    # print(f"Asr         {minsToTime(prayerTimes[3])}")
    # print(f"Maghrib     {minsToTime(prayerTimes[4])}")
    # print(f"Isha        {minsToTime(prayerTimes[5])}")

    nextPrayerNewState = nextPrayer
    while(nextPrayer==nextPrayerNewState):
        
        now = datetime.now()
        hours = now.hour
        if hours>12: hours-=12 # convert 24 hour time to 12, ex: 14 becomes 2
        if hours==0: hours=12 # midnight is 12 not 0
        timeLabel.text = f"{hours}:{str(now.minute).zfill(2)}:{str(now.second).zfill(2)}"

        currTime = f"{now.hour}:{now.minute}"
        currTimeInt = timeToMins(currTime)
        
        # check if the next prayer time is here
        for i in range(len(prayerTimes)):
            if prayerTimes[i]>currTimeInt:
                nextPrayerNewState = prayerTimes[i]
                break
    
        # Updating mins until next prayer
        if nextPrayer!=None:
            timeToNext = nextPrayer-currTimeInt
            hoursToNext = int(timeToNext/60)
            minsToNext = int(timeToNext%60)
            if hoursToNext!=0:
                nextText = f"{nextPrayerName} in {hoursToNext} hours and {minsToNext} mins"
            else: nextText = f"{nextPrayerName} in {minsToNext} mins"
        else: nextText = "All Prayers Done!"
        nextLabel.text = nextText

        sleep(.99) #wait until the next second
        #.99 because each iteration of this loop takes roughly .005 seconds


def main():
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
    
    while(1):
        now = datetime.now()
        startDate = now.day

        data = callAthanAPI(now, lats[locState], longs[locState])
        timings = data["data"]["timings"]
        prayerTimes = getTimings(timings)

        #initial currTime
        currDate = now.day

        while((currDate==startDate) and (locState==currLocState)):
            currTime = datetime.now()
            currDate = currTime.date
            outputAthan(prayerTimes, names[locState], currTime)

def initializeScreen():
    global display

    displayio.release_displays()

    spi = board.SPI()
    tft_cs = board.D22
    tft_dc = board.D24
    tft_rst = board.D25

    display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
    display = adafruit_ili9341.ILI9341(display_bus, width=WIDTH, height=HEIGHT, rotation=ROT, auto_refresh=True)
    # display = "test"

if __name__ == "__main__":
    initializeScreen()
    main()