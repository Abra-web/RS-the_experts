import sys
import time

from pytictoc import TicToc

from api_playlist import api_playlist
from song_searcher import song_searcher
from storage_handler import Storage
import evaluation2 as eval

if __name__ == '__main__':
    def print1by1(item):
        for c in item:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.01)
        print


    def print1by1_2(item):
        for c in item:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.05)
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
    input_confirmation = '\n Input received! I am now creating your personalized playlist...\n'
    hearts = "  ### ###         ### ###         ### ###         ### ###  \n #########       #########       #########       ######### \n  #######         #######         #######         #######  \n   #####           #####           #####           #####   \n    ###             ###             ###             ###    \n     #               #               #               #     \n \n"
    print1by1(input_confirmation)
    print('\n'+hearts)

    t = TicToc()
    t.tic()
    # execute functions from song_searcher file (commented there)
    rs = song_searcher(song_uris, df_song_uris, df_pl_id)

    output_song_uris, song_occurrences = rs.recommend_songs(output_size)
    a = api_playlist()
    a.call_refresh()
    tracks =''
    for element in output_song_uris:
        song_name, artist_name = a.get_song_name(element)
        tracks += str(song_occurrences[output_song_uris.index(element)]) + " times:   " + song_name + "  -  "+ artist_name + "\n"
    #tracks = tracks[:-1]
    t.toc()
    print1by1_2(rs.generate_explanation())
    print1by1_2('\n' +tracks+'\n \n')


    print1by1("Would you like to see the id's of the top matched playlists, which were used to recommend you the songs? (Y/N)")
    response=str(input())
    if response == "Y":
        best_playlists=rs.best_playlists
        response="\n The id's of the best matched playlists are as follows:\n"
        response+="\n".join(best_playlists)
        quitting=False
        reprint=True
        while not quitting:
            if reprint:
                print(response)
                print("")
                print("Would you like to see the contents of any of these playlists?\n")
                print("If yes, then input an Id of one of them you might want to inspect!")
                print("If no, input 'N' !\n")
            user_response=str(input())
            if user_response == "N":
                quitting=True
            else:
                if user_response in best_playlists:

                    requested_uris = df_pl_id[df_pl_id['pid'] == int(user_response)]['track_uri'].item().split(';')
                    for song_uri in requested_uris:
                        song_name, artist_name = a.get_song_name(song_uri)
                        print(song_name + "  -  " + artist_name)
                    #printing entire playlist
                    reprint=True
                else:
                    print("Invalid id input!")
                    reprint=False


    print("\n---------------------\n")
    # print("snipped from input content:\n")
    # for item in song_uris[0:6]:
    #     print(a.get_song_name(item))
    # print("\n---------------------\n")

    cal = eval.Evaluate(song_uris, output_song_uris)
    print1by1("The accuracy of the current prediction is:")
    print(cal.give())

    # print output, hopefully soon connected to Spotify API to add to our playlist
    #print(output_song_uris)
    #a.add_to_playlist(tracks)
    #print(a.get_name('spotify:track:7H6ev70Weq6DdpZyyTmUXk'))
    #print(a.get_features('6Sy9BUbgFse0n0LPA5lwy5'))
    # print(a.get_me())