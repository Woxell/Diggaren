import requests
import base64

class SpotifyAuthenticator:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None

    def get_access_token(self):
        auth_url = "https://accounts.spotify.com/api/token"
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(auth_url, headers=headers, data=data)
        response_data = response.json()
        self.access_token = response_data.get("access_token")
        return self.access_token

    def set_access_token(self):
        if not self.access_token:
            self.get_access_token()

    def access_token_set(self):
        return self.access_token is not None

    def search_song(self, query):
        if not self.access_token:
            self.get_access_token()
        search_url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(search_url, headers=headers)
        return response.json().get("tracks", {}).get("items", [])