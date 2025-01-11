from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


class SpotifyAuthenticator:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp_oauth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-read-private user-read-email user-read-playback-state user-modify-playback-state"
        )
        self.sp = None
    
    def get_auth_url(self):
        return self.sp_oauth.get_authorize_url()
    
    def set_access_token(self, code):
        token_info = self.sp_oauth.get_access_token(code)
        if token_info:
            self.sp = Spotify(auth=token_info['access_token'])
        else:
            raise Exception("Failed to retrieve access token")
        
    def get_current_user(self):
        if self.sp:
            try:
                return self.sp.current_user()
            except Exception as e:
                print(f"Error fetching user: {e}")
                return None
        return None