import requests
import json
from datetime import datetime
from time import sleep
import os

prayerID = {0: "Fajr", 1: "Sunrise", 2: "Duhr", 3: "Asr", 4: "Maghrib", 5: "Isha"}

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


def outputAthan(prayerTimes, locationName):
    #update currTime
    nowNow = datetime.now()
    currDate = nowNow.day
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

    os.system('cls')
    # now that everything is calculated, print them all
    print(f"     {currTime}")
    print(f"{nowNow.month}/{nowNow.day}/{nowNow.year}, {locationName}")
    #print timings as time
    print(f"Fajr        {minsToTime(prayerTimes[0])}")
    print(f"Sunrise     {minsToTime(prayerTimes[1])}")
    print(f"Duhr        {minsToTime(prayerTimes[2])}")
    print(f"Asr         {minsToTime(prayerTimes[3])}")
    print(f"Maghrib     {minsToTime(prayerTimes[4])}")
    print(f"Isha        {minsToTime(prayerTimes[5])}")

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