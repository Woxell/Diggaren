import requests
url = "https://api.sr.se/api/v2/"

def getSongName(channel):
    endpoint = f"playlists/rightnow?channelid={channel}"
    params = {"format":"json"}
    response = requests.get(url+endpoint,params=params)
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
    params = {"format":"json"}
    response = requests.get(url+endpoint,params=params)
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