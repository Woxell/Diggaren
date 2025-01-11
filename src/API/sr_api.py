import requests
from datetime import datetime

url = "https://api.sr.se/api/v2/"


def getSongInfo(channel):
    endpoint = f"playlists/rightnow?channelid={channel}"
    params = {"format": "json"}
    response = requests.get(url + endpoint, params=params)
    if response.status_code == 200:
        data = response.json()

        if 'playlist' in data and 'song' in data['playlist'] and data['playlist']['song']:
            song = data['playlist']['song']
            channelName = data.get('channel', {}).get('name', 'okänd kanal')
            title = song.get('title', 'okänd titel')
            artist = song.get('artist', 'okänd artist')
            startTime = song.get('starttimeutc', None)

            if startTime:
                startTime = datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%SZ")
                startTime = datetime.strftime("%Y-%m-%d %H:%M:%S")
            else:
                startTime = "Ingen starttid kompis"
            print(f"Kanal: {channelName}")
            print(f"Artist: {artist}")
            print(f"Låt: {title}")
            print(f"Klockslag: {startTime}")
        else:
            print("Ingen låt spelas nu kingen")
    else:
        print(f"Fel {response.status_code} : {response.text}")

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

getSongName(164)
getSongArtist(164)
getSongInfo(164)