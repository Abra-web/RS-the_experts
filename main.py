import sys
import time
from pytictoc import TicToc
from api_playlist import api_playlist
from song_searcher import SongSearcher
from storage_handler import Storage
import evaluate as eval

if __name__ == '__main__':
    def print1by1(item):
        for c in item:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.01)
        print

    def print1by1_slow(item):
        for c in item:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.05)
        print

    print("Setting up storage...")
    storage = Storage()
    print("Loading playlists...")
    df_pl_id = storage.give_playlist()
    print("Loading songs...")
    df_song_uris = storage.give_songs()
    print("Creating api connection...")
    a = api_playlist()
    a.call_refresh()

    # work with API or DATAset?
    choice = None
    counter = 0
    while counter == 0:
        choice = input("\nWould you like to use the dataset or the API as input? (data/api)")
        if choice == 'data':
            choice = 0
            counter += 1
            print("Thank you for choosing DATA.")
        elif choice == 'api':
            choice = 1
            counter += 1
            print("Thank you for choosing API.")
        else:
            print("Invalid Choice.")

    # get data for RecSys depending on choice
    num_people = 1  # init necessary for explanation
    if choice == 0:
        playlist_id = int(input('\nWhich playlist would you like to recommend songs to? !!!!Must be lower 600.000 and not in [60.000,99.999]!!!\n'))
        song_strings = df_pl_id[df_pl_id['pid'] == playlist_id]["track_uri"].item()
        song_uris = song_strings.split(';')
        print("\n---------------------")
        print("snipped from input content:\n")
        for item in song_uris[0:6]:
            song_name, artist_name = a.get_name(item)
            print(song_name + " - " + artist_name)
        print("---------------------\n")
    else:
        num_people = int(input("How many playlist do u want to give?"))
        song_strings = ''
        for i in range(num_people):
            playlist_link = input('Which playlist would you like to recommend songs to? Give the playlist link')
            playlist_URI = playlist_link.split("/")[-1].split("?")[0]
            song_strings += a.get_songs(playlist_URI)
        song_uris = song_strings.split(',')
        print('Playlist has length: ' + str(len(song_uris)))

    # input confirmation!
    output_size = int(input('How many songs would you like to have suggested?'))
    input_confirmation = '\nInput received! I am now creating your personalized playlist...\n'
    hearts = "  ### ###         ### ###         ### ###         ### ###  \n #########       #########       #########       ######### \n  #######         #######         #######         #######  \n   #####           #####           #####           #####   \n    ###             ###             ###             ###    \n     #               #               #               #     \n \n"
    print1by1(input_confirmation)
    print('\n'+hearts)

    # RecSys
    rs = SongSearcher(song_uris, df_song_uris, df_pl_id, 0.15, 10)
    output_song_uris, song_occurrences = rs.recommend_songs(output_size)


    tracks = ''
    for element in output_song_uris:
        tracks += element + ","
    for element in song_uris:
        tracks += element + ","
    tracks = tracks[:-1]

    items = ''
    for item in output_song_uris:
        song_name, artist_name = a.get_name(item)
        items += str(
            song_occurrences[output_song_uris.index(item)]) + " times:   " + song_name + "  -  " + artist_name + "\n"

    if choice == 0 or (choice == 1 and num_people == 1):
        print1by1_slow(rs.generate_explanation())
        print1by1_slow('\n' + items + '\n \n')
    elif choice == 1 and num_people > 1:
        print1by1_slow(rs.generate_group_explanation())
        print1by1_slow('\n' + items + '\n \n')

    # evaluation
    cal = eval.Evaluate(song_uris, output_song_uris)
    print1by1("The accuracy of the current prediction based on song feaatures is:\n")
    print(cal.give())


    print1by1("Would you like to investigate the content of the top matched playlists, which were used to recommend you the songs? (Y/N)")
    response = str(input())
    if response == "Y":
        best_playlists = rs.best_playlists
        response = "\nThe id's of the best matched playlists are as follows:\n"
        response += "\n".join(best_playlists)
        quitting = False
        reprint = True
        while not quitting:
            if reprint:
                print(response)
                print("")
                print("Would you like to see the contents of any of these playlists?\n")
                print("If yes, then input an Id of one of them you might want to inspect!")
                print("If no, input 'N' !\n")
            user_response = str(input())
            if user_response == "N":
                quitting = True
            else:
                if user_response in best_playlists:

                    requested_uris = df_pl_id[df_pl_id['pid'] == int(user_response)]['track_uri'].item().split(';')
                    print("\n---------------------")
                    for song_uri in requested_uris:
                        song_name, artist_name = a.get_name(song_uri)
                        print(song_name + "  -  " + artist_name)
                    print("---------------------\n")
                    reprint = True
                else:
                    print("Invalid id input!")
                    reprint = False
    print("\n---------------------\n")

    # add to playlist
    if choice == 1:
        add = input("Would you like to add the suggested songs to a playlist? (Y/N)")
        if add == 'Y':
            # a.add_to_playlist(tracks)
            print("Successfully added to playlist!")
        else:
            print("Thank you for using our recommender system. Have a nice day!")


