from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

#client_id, client_secret, redirect_uri är nödvändiga för att användaren ska kunna autentisera med Spotify API
class SpotifyAuthenticator:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp_oauth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-read-private user-read-email user-read-playback-state user-modify-playback-state" #Definierar vilka behörigheter som begärs från användaren
        )
        self.sp = None #Håller instansen av den autentiserade Spotify-klienten
    
    #Genererar en URL som användaren kan besöka för att logga in med sitt personliga Spotify-konto
    def get_auth_url(self):
        return self.sp_oauth.get_authorize_url()
    
    #Använder auktoriseringskoden för att få en access-token
    def set_access_token(self, code):
        token_info = self.sp_oauth.get_access_token(code)
        if token_info:
            self.sp = Spotify(auth=token_info['access_token'])
        else:
            raise Exception("Failed to retrieve access token")
        
    #Hämtar information om den aktuella användaren (om Spotify-instansen är autentiserad)
    def get_current_user(self):
        if self.sp:
            try:
                return self.sp.current_user()
            except Exception as e:
                print(f"Error fetching user: {e}")
                return None
        return None
    
    #Söker efter låtar på Spotify baserat på en sökfråga (som i denna kod är kopplad till queryn SverigesRadio)
    def search_song(self, query):
        if self.sp:
            try:
                results = self.sp.search(q=query, type='track', limit=5)
                tracks = results.get('tracks', {}).get('items', [])
                return [
                    {
                        "name": track['name'],
                        "artist": ", ".join(artist['name'] for artist in track['artists']),
                        "spotify_url": track['external_urls']['spotify'],
                        "album": track['album']['name']
                    }
                    for track in tracks
                ]
            except Exception as e:
                print(f"Error searching song: {e}")
                return None
        else:
            print("Spotify-klienten är inte autentiserad.")
            return None