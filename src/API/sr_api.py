import requests
url = "https://api.sr.se/api/v2/"

def getSongName(channel):
    response = requests.get(url+"/channels?format=json")


