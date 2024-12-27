import requests
import json
import datetime
from datetime import datetime
import os
from time import sleep

def callAPI(currTime, lat, long):
    #method 2 is North America Islamic Association's method for deciding athan time
    url = f"https://api.aladhan.com/v1/timings/{currTime.month}-{currTime.day}-{currTime.year}"
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
    isha = int(timeToMins(timings["Isha"]))
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

# define prayer IDs
prayerID = {0: "Fajr", 1: "Sunrise", 2: "Duhr", 3: "Asr", 4: "Maghrib", 5: "Isha"}

# define states
DAVIS = 0
SC = 1
SPOTIFY = 2
CALC = 3

# initial values
currState = 1

while(1): #runs forever
    state=currState
    if state==DAVIS:
        latitude = 38.54491
        longitude = -121.74052
        place = "Davis"
    elif state==SC:
        latitude = 37.35411
        longitude = -121.95524
        place = "Santa Clara"

    while(state==currState): #this checks every 5 mins
        now = datetime.now()
        startDate = now.day
        startTime = f"{now.hour}:{now.minute}"
        startTimeInt = timeToMins(startTime)
        # now = datetime.fromtimestamp(1735328028)

        # print("calling api now")
        data = callAPI(now, latitude, longitude)
        timings = data["data"]["timings"]

        prayerTimes = getTimings(timings)

        #initial currTime
        currDate = now.day
        currTime = f"{now.hour}:{now.minute}"
        currTimeInt = timeToMins(currTime)

        #when the touchscreen gets added, have that change the state, then this code will also check that state==currState
        while((currDate==startDate) and (state==currState)): # only break this loop at midnight when the day changes

            #update currTime
            nowNow = datetime.now()
            currDate = nowNow.day
            currTime = f"{nowNow.hour}:{nowNow.minute}"
            currTimeInt = timeToMins(currTime)
            
            # check if the next prayer time is here
            nextPrayer = None
            nextPrayerName = None
            for i in range(len(prayerTimes)):
                if prayerTimes[i]>currTimeInt:
                    nextPrayer = prayerTimes[i]
                    nextPrayerName = prayerID.get(i)
                    break

            if nextPrayer!=None:
                timeToNext = nextPrayer-currTimeInt
                hoursToNext = int(timeToNext/60)
                minsToNext = int(timeToNext%60)

            os.system('cls')

            # now that everything is calculated, print them all
            print(f"     {minsToTime(timeToMins(currTime)).strip()}:{nowNow.second}") #mins to time then time to mins is the easiest way to convert from 24 to 12 hour
            print(f"{now.month}/{now.day}/{now.year}, {place}")
            #print timings as time
            print(f"Fajr        {minsToTime(prayerTimes[0])}")
            print(f"Sunrise     {minsToTime(prayerTimes[1])}")
            print(f"Duhr        {minsToTime(prayerTimes[2])}")
            print(f"Asr         {minsToTime(prayerTimes[3])}")
            print(f"Maghrib     {minsToTime(prayerTimes[4])}")
            print(f"Isha        {minsToTime(prayerTimes[5])}")

            if nextPrayer!=None:
                if hoursToNext!=0:
                    print(f"{nextPrayerName} in {hoursToNext} hours and {minsToNext} minutes")
                else: print(f"{nextPrayerName} in {minsToNext} minutes")
            else: print("All Prayers Complete!")

            sleep(1) #wait before updating settings

