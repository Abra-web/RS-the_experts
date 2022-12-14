import sys
import time
from storage_handler import Storage
from song_searcher import SongSearcher
from pytictoc import TicToc
from api_playlist import api_playlist

if __name__ == '__main__':
    t = TicToc()
    t.tic()
    storage = Storage()
    a = api_playlist()
    a.call_refresh()
    print("Loading playlists...")
    df_pl_id = storage.give_playlist()
    print("Loading songs...")
    df_song_uris = storage.give_songs()
    num_people = int(input("How many playlist do u want to give?"))
    song_strings = ''
    for i in range(num_people):
        playlist_link = input('Which playlist would you like to recommend songs to? Give the playlist link')
        playlist_URI = playlist_link.split("/")[-1].split("?")[0]
        song_strings += a.get_songs(playlist_URI)
    song_uris = song_strings.split(',')
    print('Playlist has length: ' + str(len(song_uris)))
    print("recommending songs and exiting main...")
    # execute functions from song_searcher file (commented there)
    rs = SongSearcher(song_uris, df_song_uris, df_pl_id, 0.2, 10)

    print("found songs...")
    output_song_uris = rs.recommend_songs(5)
    tracks = ''
    for element in output_song_uris:
        tracks += element + ","
    for element in song_uris:
        tracks += element + ","
    tracks = tracks[:-1]

    print(rs.generate_explanation())
    for item in output_song_uris[0:6]:
        print(a.get_name(item))

    t.toc()
    # a.add_to_playlist(tracks)
