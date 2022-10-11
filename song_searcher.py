import random

import pandas as pd


class song_searcher:

    def __init__(self, input_song_uris, df_song_uri, df_playlist_id):
        self.input_song_uris = input_song_uris
        self.df_song_uri = df_song_uri
        self.df_playlist_id = df_playlist_id

    def recommend_songs(self, sample_size):

        playlist_collection = self.song_searcher()
        print(playlist_collection[1:10])
        print(len(playlist_collection))
        sorted_playlist_dictionary = self.playlist_counter(playlist_collection)
        return self.song_suggester(sorted_playlist_dictionary, sample_size)

    # returns a list of how many times a song appears in all playlists, playlist_id will be in the list
    # if song appears in n playlists, playlist_id will be in the list n-times
    def song_searcher(self):
        print("entering song searcher")
        playlist_id_collection = []
        songs_error = []
        for uri in self.input_song_uris:
            try:
                playlist_id_collection.append(self.df_song_uri.get(uri))
            except:
                songs_error.append(uri)
                print('song was not in our database')

        #  flatten the nested playlist collection list
        flat_list = [i for b in map(lambda x: [x] if not isinstance(x, list) else x, playlist_id_collection) for i in b]

        #  extract the playlist ids out of every playlist collection
        separated_list = []
        for element in flat_list:
            separated_list.append(element.split(';'))

        # flatten created nested list again to get ['id1', 'id2', ...]
        separated_list = [i for b in map(lambda x: [x] if not isinstance(x, list) else x, separated_list) for i in b]
        print("exiting song searcher...")
        return separated_list

    # output: ordered dict of key: playlist_id, value: similar songs/length of playlist
    def playlist_counter(self, separated_list):
        print("entering playlist counter ... ")
        li = []
        for playlist_id in set(separated_list):
            print(int(playlist_id))
            song_uris = self.df_playlist_id[self.df_playlist_id['pid'] == int(playlist_id)]['track_uri'].item().split(';')
            li.append((int(playlist_id), separated_list.count(playlist_id)/len(song_uris)))
        playlist_dictionary = dict(li)
        #the dict doesnt have to exist twice it can be generated in the loop
        #playlist_dictionary = dict(
        #    (playlist_id, separated_list.count(playlist_id) / length_playlist[int(playlist_id)]) for playlist_id in set(separated_list))
        sorted_playlist_dict = {key: val for key, val in
                                sorted(playlist_dictionary.items(), key=lambda ele: ele[1], reverse=True)}

        #remove first item from the dict:  this is the input playlist we dont want to use
        (k := next(iter(sorted_playlist_dict)), sorted_playlist_dict.pop(k))
        return sorted_playlist_dict

    # sample_size: number of songs u want to recommend, sorted_playlist_dict: ordered dict of key: playlist_id, value: similar songs/length of playlist
    # outputs a list with the song uris
    def song_suggester(self, sorted_playlist_dict, sample_size):
        best_match_playlist = []
        loop_counter = 0;
        for playlist_id in sorted_playlist_dict:
            if loop_counter == 4:
                best_match_playlist.append(self.df_playlist_id[self.df_playlist_id['pid'] == int(playlist_id)]['track_uri'].item().split(';'))
                break
            else:
                best_match_playlist.append(
                    self.df_playlist_id[self.df_playlist_id['pid'] == int(playlist_id)]['track_uri'].item().split(';'))

            loop_counter +=1
        best_match_playlists_song_uris_flatlist = [i for b in map(lambda x: [x] if not isinstance(x, list) else x, best_match_playlist) for i in b]
        #best_match_playlist_list = best_match_playlist.split(';')  # stores all the songs of the 5 best playlists
        res = sorted(set(best_match_playlists_song_uris_flatlist), key=lambda x: best_match_playlists_song_uris_flatlist.count(x),
                     reverse=True)  # sort songs_urls based on how many times the song appears in the 5 best playlists
        res = [x for x in res if x not in self.input_song_uris]  # remove the songs from the original playlist
        output_song_uris = res[:sample_size]  # get the n best songs that will be recommended
        songs_occurences = []
        for i in output_song_uris:
            songs_occurences.append(best_match_playlists_song_uris_flatlist.count(i))
        return output_song_uris
