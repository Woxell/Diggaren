import requests
from datetime import datetime

url = "https://api.sr.se/api/v2/"

def getLastSong(channel):
    endpoint = f"playlists/rightnow?channelid={channel}"
    params = {"format": "json"}
    response = requests.get(url + endpoint, params=params)
    if response.status_code == 200:
        data = response.json()

        if 'playlist' in data and 'previoussong' in data['playlist']:
            song = data['playlist']['previoussong']
            channelName = data.get('playlist', {}).get('channel', {}).get('name', 'okänd kanal')
            title = song.get('title', 'okänd titel')
            artist = song.get('artist', 'okänd artist')
            startTime = song.get('starttimeutc', None)
            stopTime = song.get('stoptimeutc', None)
            if startTime:
                timestamp_ms = int(startTime.strip("/Date()"))
                startTime = datetime.fromtimestamp(timestamp_ms / 1000)  # Konvertera till sekunder
                startTime = startTime.strftime("%Y-%m-%d %H:%M:%S")

                timestamp_ms2 = int(stopTime.strip("/Date()"))
                stopTime = datetime.fromtimestamp(timestamp_ms2 / 1000)  # Konvertera till sekunder
                stopTime = stopTime.strftime("%Y-%m-%d %H:%M:%S")

            else:
                startTime = "Ingen starttid kompis"
                stopTime = "Ingen stopptid kombis"
            print(f"Kanal: {channelName}")
            print(f"Artist: {artist}")
            print(f"Låt: {title}")
            print(f"Starttid: {startTime}")
            print(f"Stopptid: {stopTime}")
        else:
            print("Ingen låt spelas nu kingen")
    else:
        print(f"Fel {response.status_code} : {response.text}")

getLastSong(164)