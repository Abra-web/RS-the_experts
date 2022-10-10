from storage_handler import Storage, join, DIR_DATA_CSV, DIR_DATA_JSON, Type
import glob
from file_processor import process_all

from api_playlist import api_playlist

from song_searcher import song_searcher

if __name__ == '__main__':


    storage = Storage()
    df_pl_id = storage.give_playlist()
    df_song_uris = storage.give_songs()
    print('Which playlist would you like to recommend songs too?')
    playlist_id = input()
    song_strings = df_pl_id[12330]
    song_uris = song_strings.split(';')

    # execute functions from song_searcher file (commented there)
    rs = song_searcher(song_uris, df_song_uris, df_pl_id)
    output_song_uris = rs.recommend_songs(5)

    #a = api_playlist()
    #a.call_refresh()
    tracks =''
    for element in output_song_uris:
        tracks += element+","
    tracks = tracks[:-1]

    # print output, hopefully soon connected to Spotify API to add to our playlist
    #print(output_song_uris)
    #a.add_to_playlist(tracks)
    #print(a.get_name('spotify:track:7H6ev70Weq6DdpZyyTmUXk'))
    #print(a.get_features('6Sy9BUbgFse0n0LPA5lwy5'))
    #print(a.get_me())

