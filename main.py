from storage_handler import Storage, join, DIR_DATA_CSV, DIR_DATA_JSON, Type
from pytictoc import TicToc
import glob
from file_processor import process_all

from api_playlist import api_playlist
import numpy

from song_searcher import song_searcher

if __name__ == '__main__':
    t = TicToc()
    t.tic()
    storage = Storage()
    print("Loading playlists...")
    df_pl_id = storage.give_playlist()
    print("Loading songs...")
    df_song_uris = storage.give_songs()
    playlist_id = int(input('Which playlist would you like to recommend songs to? ATTENTION:LOWER 590.000!!!'))
    print('input received. Getting playlist...')
    song_strings = df_pl_id[df_pl_id['pid'] == playlist_id]["track_uri"].item()
    print('input received. Prepping playlist for use...')
    song_uris = song_strings.split(';')

    print("recommending songs and exiting main...")
    # execute functions from song_searcher file (commented there)
    rs = song_searcher(song_uris, df_song_uris, df_pl_id)

    print("found songs...")
    output_song_uris = rs.recommend_songs(5)

    #a = api_playlist()
    #a.call_refresh()
    tracks =''
    for element in output_song_uris:
        tracks += element+","
    tracks = tracks[:-1]
    print(tracks)
    t.toc()
    # print output, hopefully soon connected to Spotify API to add to our playlist
    #print(output_song_uris)
    #a.add_to_playlist(tracks)
    #print(a.get_name('spotify:track:7H6ev70Weq6DdpZyyTmUXk'))
    #print(a.get_features('6Sy9BUbgFse0n0LPA5lwy5'))
    #print(a.get_me())

