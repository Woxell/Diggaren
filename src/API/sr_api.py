import requests
url = "https://api.sr.se/api/v2/"

def getSongName(channel):
    endpoint = f"channels/{channel}/playlists/rightnow"
    params = {"format":"json"}
    response = requests.get(url+endpoint,params=params)
    if response.status_code == 200:
        data = response.json()
        if 'song' in data and data['song']:
            song = data['song']
            print(f"Title: {song['title']}")
        else:
            print(f"No song playing")
    else:
        print(f"error {response.status_code}: {response.text}")

getSongName(164)