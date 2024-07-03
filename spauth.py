import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv
load_dotenv()

client_credentials_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)