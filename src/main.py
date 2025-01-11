import os.path

import requests
from flask import Flask, request, redirect, session, jsonify, render_template
from spotify_auth import SpotifyAuthenticator

app = Flask(__name__)
app.secret_key = 'en_hemlig_nyckeln'


file_path = os.path.abspath('../../src/spotify-api-key.txt')
with open(file_path, "r") as file:
    for line in file:
        if line.startswith("API_KEY="):
            api_key = line.split("=", 1)[1].strip()
        elif line.startswith("API_SECRET="):
            api_secret = line.split("=", 1)[1].strip()

SPOTIPY_CLIENT_ID = api_key
SPOTIPY_CLIENT_SECRET = api_secret
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'
spotify_auth = SpotifyAuthenticator(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)


# sr
# sr_auth = SRAuth()

@app.route('/')
def index():
    auth_url = spotify_auth.get_auth_url()

    try:
        response = requests.get('http://api.sr.se/api/v2/channels?format=json')
        data = response.json()

        channels = data.get("channels", [])  # få ut alla channel-objekt ur json-datan som en array

        li_components = "".join(  # Skapa en lista av <li>-komponenter för varje radiokanal
            f"""
            <li onclick="displayStation({channel})">
                <a target="_blank">{channel.get('name')}</a>
                <p>{channel.get('tagline')}</p>
            </li>
            """ for channel in channels)  # for-each loop

    except requests.RequestException as e:
        print(f"Error: {e}")

        li_components = "<li>API ligger nere?.</li>"

    return render_template('dashboard.html', radio_list=li_components)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    print(f"Recieved code: {code}")
    if not code:
        return "Ingen kod mottogs från Spotify", 400

    try:
        spotify_auth.set_access_token(code)
        print("Access token satt!")
        return redirect('/dashboard')
    except Exception as e:
        print(f"Error setting access token: {e}")
        return "Ett fel uppstod vid autentisering", 500


@app.route('/dashboard')
def dashboard():
    # SR
    try:
        response = requests.get('http://api.sr.se/api/v2/channels?format=json')
        data = response.json()

        channels = data.get("channels", [])  # få ut alla channel-objekt ur json-datan som en array

        li_components = "".join(  # Skapa en lista av <li>-komponenter för varje radiokanal
            f"""
            <li>
                <a href="{channel.get('siteurl')}" target="_blank">{channel.get('name')}</a>
                <p>{channel.get('tagline')}</p>
            </li>
            """ for channel in channels)  # for-each loop

    except requests.RequestException as e:
        print(f"Error: {e}")

        li_components = "<li>API ligger nere?.</li>"

    # Spotify
    try:
        user_info = spotify_auth.get_current_user()
        print(f"User info: {user_info}")
        if user_info:
            return render_template('dashboard.html', radio_list=li_components, user=user_info)
        return redirect('/')
    except Exception as e:
        print(f"Error fetching user info: {e}")
        return "Ett fel uppstod vid hämtning av användarinformation", 500


if __name__ == '__main__':
    app.run(debug=True)
