import os
import requests
from collections import deque
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from spotify_auth import SpotifyAuthenticator

app = Flask(__name__)
app.secret_key = 'en_hemlig_nyckeln'

CORS(app)

# # Read API keys
api_key = os.environ['API_KEY']
api_secret = os.environ['API_SECRET']

spotify_auth = SpotifyAuthenticator(api_key, api_secret)

# Index, simulerar Spotify user login
@app.route('/')
def index():
    if spotify_auth.access_token_set():
        return redirect('/dashboard')
    return render_template('index.html')


# Metod för att hantera callback efter autentisering hos Spotify
# @app.route('/callback')
# def callback():
#     code = request.args.get('code')
#     print(f"Recieved code: {code}")
#     if not code:
#         return "Ingen kod mottogs från Spotify", 400
#
#     try:
#         spotify_auth.set_access_token(code)
#         print("Access token satt!")
#         return redirect('/dashboard')
#     except Exception as e:
#         print(f"Error setting access token: {e}")
#         return "Ett fel uppstod vid autentisering", 500

# Main dashboard. Använder ej längre spotify-användare
@app.route('/dashboard')
def dashboard():
    spotify_auth.set_access_token()
    return render_template('dashboard.html')

@app.errorhandler(404)
def page_not_found(error):
    print(error)
    return render_template('404.html'), 404

@app.route('/api')
def api_dox():
    return render_template('api.html')

###REST-metoder
@app.route('/channels', methods=['GET'])
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

#Här lagrar vi sökresultat som en kö, max 5 sparade sökresultat
search_queries = deque(maxlen=5)

@app.route('/result', methods=['GET'])
def search_song():
    title = request.args.get('title')
    artist = request.args.get('artist')

    if title and artist:
        search_query = f"{title} {artist}"
        try:
            search_results = spotify_auth.search_song(search_query)
            search_queries.append(search_results[0])  # Spara endast första sökresultatet
            return jsonify({"message": "Search successful", "results": search_results}), 200
        except Exception as e:
            print(f"Error searching Spotify: {e}")
            return jsonify({"error": "Error occurred while searching Spotify"}), 500
    else:
        # Returnera sparade sökningar om inga query-parametrar anges
        return jsonify({"saved_searches": list(search_queries)}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8080)