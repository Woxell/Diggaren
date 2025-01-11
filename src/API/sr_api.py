import requests
from datetime import datetime

url = "https://api.sr.se/api/v2/"
testChanel = 164
def getChannel(channel):
    endpoint = f"playlists/rightnow?channelid={channel}"
    params = {"format": "json"}
    response = requests.get(url + endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'playlist' in data and 'channel' in data['playlist']:
            channelName = data.get('playlist', {}).get('channel', {}).get('name', 'okänd kanal')
            return channelName
        else:
            return "Vet ej brudda"
    else:
        return f"error {response.status_code}: {response.text}"

def getSongName(channel):
    endpoint = f"playlists/rightnow?channelid={channel}"
    params = {"format": "json"}
    response = requests.get(url + endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'playlist' in data and 'song' in data['playlist'] and data['playlist']['song']:
            song = data['playlist']['song']
            return song['title']
        else:
            return "No song playing"
    else:
        return f"error {response.status_code}: {response.text}"


def getSongArtist(channel):
    endpoint = f"playlists/rightnow?channelid={channel}"
    params = {"format": "json"}
    response = requests.get(url + endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'playlist' in data and 'song' in data['playlist'] and data['playlist']['song']:
            song = data['playlist']['song']
            return song['artist']
        else:
            return "No song playing"
    else:
        return f"error {response.status_code}: {response.text}"

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
            return startTime
        else:
            return "Komigen kombis den har inte startat"
    else:
        return f"error {response.status_code}: {response.text}"


print(getChannel(testChanel))
print(getSongName(testChanel))
print(getSongArtist(testChanel))
print(getStartTime(testChanel))
