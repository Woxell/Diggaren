import requests
from flask import Flask, request, redirect, session, jsonify, render_template
from spotify_auth import SpotifyAuthenticator

app = Flask(__name__)
app.secret_key = 'en_hemlig_nyckeln'

SPOTIPY_CLIENT_ID = 'client-id'
SPOTIPY_CLIENT_SECRET = 'client-server'
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'
spotify_auth = SpotifyAuthenticator(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)


# sr
# sr_auth = SRAuth()

@app.route('/')
def index():
    try:
        response = requests.get('http://api.sr.se/api/v2/channels?format=json')
        data = response.json()

        channels = data.get("channels", [])

        li_components = "".join(
            f"""
            <li>
                <a href="{channel.get('siteurl')}" target="_blank">{channel.get('name')}</a>
                <p>{channel.get('tagline')}</p>
            </li>
            """
            for channel in channels
        )

    except requests.RequestException as e:
        print(f"Error: {e}")

        li_components = "<li>API ligger nere?.</li>"

    auth_url = spotify_auth.get_auth_url()

    return render_template('index.html', radio_list=li_components, auth_url=auth_url)


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
    try:
        user_info = spotify_auth.get_current_user()
        print(f"User info: {user_info}")
        if user_info:
            return render_template('dashboard.html', user=user_info)
        return redirect('/')
    except Exception as e:
        print(f"Error fetching user info: {e}")
        return "Ett fel uppstod vid hämtning av användarinformation", 500


if __name__ == '__main__':
    app.run(debug=True)
