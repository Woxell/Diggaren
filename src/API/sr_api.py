import requests
from datetime import datetime

url = "https://api.sr.se/api/v2/"

def getChannel(channel):
    endpoint = f"playlists/rightnow?channelid={channel}"
    params = {"format": "json"}
    response = requests.get(url + endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'playlist' in data and 'channel' in data['playlist']:
            channelName = data.get('playlist', {}).get('channel', {}).get('name', 'okänd kanal')
            print(f"Kanal: {channelName}")
        else:
            print(f"Vet ej brudda")
    else:
        print(f"error {response.status_code}: {response.text}")

def getSongName(channel):
    endpoint = f"playlists/rightnow?channelid={channel}"
    params = {"format": "json"}
    response = requests.get(url + endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'playlist' in data and 'song' in data['playlist'] and data['playlist']['song']:
            song = data['playlist']['song']
            print(f"Title: {song['title']}")
        else:
            print(f"No song playing")
    else:
        print(f"error {response.status_code}: {response.text}")


def getSongArtist(channel):
    endpoint = f"playlists/rightnow?channelid={channel}"
    params = {"format": "json"}
    response = requests.get(url + endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'playlist' in data and 'song' in data['playlist'] and data['playlist']['song']:
            song = data['playlist']['song']
            print(f"Artist: {song['artist']}")
        else:
            print(f"No song playing")
    else:
        print(f"error {response.status_code}: {response.text}")

def getStartTime(channel):
    endpoint = f"playlists/rightnow?channelid={channel}"
    params = {"format": "json"}
    response = requests.get(url + endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'playlist' in data and 'song' in data['playlist']:
            song = data['playlist']['song']
            startTime = song.get('starttimeutc', None)
            if startTime:
                timestamp_ms = int(startTime.strip("/Date()"))
                startTime = datetime.fromtimestamp(timestamp_ms / 1000)  # Konvertera till sekunder
                startTime = startTime.strftime("%Y-%m-%d %H:%M:%S")
            else:
                startTime = "Komigen kombis den har inte startat"
            print(f"Startid: {startTime}")
        else:
            print(f"Komigen kombis den har inte startat")
    else:
        print(f"error {response.status_code}: {response.text}")


getChannel(164)
getSongName(164)
getSongArtist(164)
getStartTime(164)