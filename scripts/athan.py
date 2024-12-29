import requests
import json

#Athan Funcs
def callAthanAPI(currTime, lat, long):
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


