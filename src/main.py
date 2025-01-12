import os.path

import requests
from flask import Flask, request, redirect, session, jsonify, render_template
from flask_cors import CORS
from spotify_auth import SpotifyAuthenticator

app = Flask(__name__)
app.secret_key = 'en_hemlig_nyckeln'  # ???

CORS(app)

# Läs in api-nycklar
file_path = os.path.abspath('../../src/spotify-api-key.txt')
with open(file_path, "r") as file:
    for line in file:
        if line.startswith("API_KEY="):
            api_key = line.split("=", 1)[1].strip()
        elif line.startswith("API_SECRET="):
            api_secret = line.split("=", 1)[1].strip()

spotify_auth = SpotifyAuthenticator(api_key, api_secret, 'http://localhost:5000/callback')

# Index
@app.route('/')
def index():
    return render_template('index.html', auth_url=spotify_auth.get_auth_url())


# Metod för att hantera callback efter autentisering hos Spotify
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
    # Spotify
    try:
        user_info = spotify_auth.get_current_user()
        print(f"User info: {user_info}")
        if user_info:
            return render_template('dashboard.html', user=user_info)
        return redirect('/')
    except Exception as e:
        print(f"Error fetching user info: {e}")
        return "Ett fel uppstod vid hämtning av användarinformation", 500

###REST-metoder
@app.route('/radio', methods=['GET'])
def get_root():
    try:
        response = requests.get('http://api.sr.se/api/v2/channels?format=json')
        return jsonify(response.json())

    except requests.RequestException as e:
        print(f"Error: {e}")
        return jsonify({"error": "Kunde inte hämta radiostationer"}), 404


@app.route('/radio/<channelID>', methods=['GET'])
def get_channel(channelID):
    try:
        response = requests.get(f"https://api.sr.se/api/v2/playlists/rightnow?channelid={channelID}&format=json")
        return jsonify(response.json())

    except requests.RequestException as e:
        print(f"ERROR: {e}")
        return jsonify({"error": "Kunde inte hämta radiostationen"}), 404

#Här lagrar vi sökresultat
search_queries = []

@app.route('/result', methods=['POST', 'OPTIONS'])
def post_search():
    if request.method == 'OPTIONS':
        return jsonify({"message": "CORS preflight passed"}), 200

    try:
        data = request.get_json()
        artist = data.get('artist')
        title = data.get('title')

        if not artist or not title:
            return jsonify({"error": "Both 'artist' and 'title' are required"}), 400

        search_query = f"{title} {artist}"
        try:
            search_results = spotify_auth.search_song(search_query)
            search_queries.append(search_results[0]) #spara endast första sökresultatet
            return jsonify({"message": "Search successful", "results": search_results}), 200

        except Exception as e:
            print(f"Error searching Spotify: {e}")
            return jsonify({"error": "Error occurred while searching Spotify"}), 500

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "Invalid request format"}), 400

@app.route('/result', methods=['GET'])
def get_search():
    return jsonify(search_queries)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
