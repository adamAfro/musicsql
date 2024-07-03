import sys, os, argparse # Import argparse

if __file__:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.abspath('../'))

from spauth import spotify
from syrics.api import Spotify as Lyrics

parser = argparse.ArgumentParser(description='Pobierz teksty piosenek dla danego artysty.')
parser.add_argument('link', type=str, help='Link artysty ze spotify')
parser.add_argument('csv', type=str, help='Plik docelowy, do którego zapisane zostaną teksty')
args = parser.parse_args()

print('Podaj coockie: ')
api = Lyrics(input()) # https://github.com/akashrchandran/syrics/wiki/Finding-sp_dc

def get_artist_songs(artist_link):
    
    artist_id = artist_link.split('/')[-1].split('?')[0]
    
    albums = []
    results = spotify.artist_albums(artist_id, album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])
    
    songs = []
    for album in albums:
        results = spotify.album_tracks(album['id'])
        tracks = results['items']
        for track in tracks:
            songs.append(track)
    
    return songs

def get_artist_lyrics(songs:list):
    
    captions = []
    for song in songs:

        lyrics = api.get_lyrics(song['id'])
        if lyrics is None: continue
        lyrics = lyrics['lyrics']

        lang = lyrics['language']
        lines = lyrics['lines']
        n = len(lines)
        if n == 0: continue
        for i in range(n):

            try:
                lines[i]['title'] = song['name']
                lines[i]['lang'] = lang
            except: pass

        captions.extend(lines)

    from pandas import DataFrame
    return DataFrame(captions)
    
songs = get_artist_songs(args.link)
captions = get_artist_lyrics(songs)
captions.to_csv(args.csv, index=False)