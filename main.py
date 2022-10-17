import sys
import time
from pytictoc import TicToc
from api_playlist import api_playlist
from song_searcher import song_searcher
from storage_handler import Storage
import evaluation as eval

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
    print(str(len(song_uris)))
    input_confirmation = '\n Input received! I am now creating your personalized playlist...\n'
    hearts = "  ### ###         ### ###         ### ###         ### ###  \n #########       #########       #########       ######### \n  #######         #######         #######         #######  \n   #####           #####           #####           #####   \n    ###             ###             ###             ###    \n     #               #               #               #     \n \n"
    print1by1(input_confirmation)
    print('\n'+hearts)

    t = TicToc()
    t.tic()
    # execute functions from song_searcher file (commented there)
    rs = song_searcher(song_uris, df_song_uris, df_pl_id,0.15,10)

    output_song_uris = rs.recommend_songs(output_size)

    a = api_playlist()
    a.call_refresh()
    tracks =''
    for element in output_song_uris:
        tracks += element+","
    for element in song_uris:
        tracks += element+","
    tracks = tracks[:-1]

    print1by1(rs.generate_explanation())
    for item in output_song_uris[0:6]:
        print(a.get_name(item))

    cal = eval.Evaluate(song_uris, output_song_uris)
    print(cal.give())
    t.toc()
    #a.add_to_playlist(tracks)

