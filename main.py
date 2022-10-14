import sys
import time

from pytictoc import TicToc

from api_playlist import api_playlist
from song_searcher import song_searcher
from storage_handler import Storage

if __name__ == '__main__':
    def print1by1(item):
        for c in item:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.01)
        print

    storage = Storage()
    print("Loading playlists...")
    df_pl_id = storage.give_playlist()
    print("Loading songs...\n")
    df_song_uris = storage.give_songs()
    playlist_id = int(input('Which playlist would you like to recommend songs to? !!!!Must be lower 600.000 and not in [60.000,99.999]!!!\n'))
    output_size = int(input('How many songs would you like to have suggested?'))
    song_strings = df_pl_id[df_pl_id['pid'] == playlist_id]["track_uri"].item()
    song_uris = song_strings.split(';')
    song_uris = ['spotify:track:5lKkgKB4yZ6BW0Aps1CKcL?si=f87d575a3ada4e4e']
    input_confirmation = '\n Input received! I am now creating your personalized playlist...\n'
    hearts = "  ### ###         ### ###         ### ###         ### ###  \n #########       #########       #########       ######### \n  #######         #######         #######         #######  \n   #####           #####           #####           #####   \n    ###             ###             ###             ###    \n     #               #               #               #     \n \n"
    print1by1(input_confirmation)
    print('\n'+hearts)

    t = TicToc()
    t.tic()
    # execute functions from song_searcher file (commented there)
    rs = song_searcher(song_uris, df_song_uris, df_pl_id)

    output_song_uris = rs.recommend_songs(output_size)

    a = api_playlist()
    a.call_refresh()
    tracks =''
    for element in output_song_uris:
        tracks += element+"\n"
    tracks = tracks[:-1]

    print1by1(rs.generate_explanation())
    print1by1('\n' +tracks+'\n \n')

    for item in output_song_uris:
        print(a.get_name(item))

    print("\n---------------------\n")
    print("snipped from input content:\n")
    for item in song_uris[0:6]:
        print(a.get_name(item))
    print("\n---------------------\n")
    t.toc()

    # print output, hopefully soon connected to Spotify API to add to our playlist
    #print(output_song_uris)
    #a.add_to_playlist(tracks)
    #print(a.get_name('spotify:track:7H6ev70Weq6DdpZyyTmUXk'))
    #print(a.get_features('6Sy9BUbgFse0n0LPA5lwy5'))
    # print(a.get_me())