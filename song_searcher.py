import random

import pandas as pd

from collections import Counter


class SongSearcher:

    def __init__(self, input_song_uris, df_song_uri, df_playlist_id, norm_threshold, list_length):
        self.input_song_uris = input_song_uris
        self.df_song_uri = df_song_uri
        self.df_playlist_id = df_playlist_id
        self.threshold = norm_threshold
        self.list_length = list_length

    def recommend_songs(self, sample_size):
        playlist_collection = self.song_searcher()
        sorted_playlist_dictionary = self.playlist_counter(playlist_collection)
        return self.song_suggester(sorted_playlist_dictionary, sample_size)

    # returns a list of how many times a song appears in all playlists, playlist_id will be in the list
    # if song appears in n playlists, playlist_id will be in the list n-times
    def song_searcher(self):
        playlist_id_collection = []
        songs_error = []
        for uri in self.input_song_uris:
            uris = self.df_song_uri.get(uri)
            if uris is not None:
                playlist_id_collection.append(uris)
            else:
                songs_error.append(uri)

        # print(str(len(songs_error))+" songs were not in our database.")

        #  flatten the nested playlist collection list
        flat_list = [i for b in map(lambda x: [x] if not isinstance(x, list) else x, playlist_id_collection) for i in b]

        #  extract the playlist ids out of every playlist collection
        separated_list = []
        for element in flat_list:
            separated_list.append(element.split(';'))

        # flatten created nested list again to get ['id1', 'id2', ...]
        separated_list = [i for b in map(lambda x: [x] if not isinstance(x, list) else x, separated_list) for i in b]
        return separated_list

    # output: ordered dict of key: playlist_id, value: similar songs/length of playlist
    def playlist_counter(self, separated_list):
        # dictionary of playlists
        counted_playlists = dict(Counter(separated_list))
        new = []

        for playlist_id in counted_playlists.keys():
            value = counted_playlists[playlist_id]/self.df_playlist_id[self.df_playlist_id['pid'] == int(playlist_id)]['num_tracks'].item()
            if value > self.threshold and value != 1:
                new.append((int(playlist_id), value))
                if len(new) > self.list_length:
                    break
        #JANS CODE
        # li.sort(key=lambda i: i[1], reverse=True)
        # print(li)
        # return dict(li)
        #MY CODE
        # sorting in next step
        return dict(new)


    # sample_size: number of songs u want to recommend, sorted_playlist_dict: ordered dict of key: playlist_id, value: similar songs/length of playlist
    # outputs a list with the song uris
    def song_suggester(self, counted_playlists, sample_size):
        #JANS CODE
        #sorted_playlist_dict = lis
        playlist_dictionary = counted_playlists
        sorted_playlist_dict = {key: val for key, val in
                                sorted(playlist_dictionary.items(), key=lambda ele: ele[1], reverse=True)}
        # remove first item from the dict:  this is the input playlist we don't want to use
        (k := next(iter(sorted_playlist_dict)), sorted_playlist_dict.pop(k))
        best_match_playlist = []
        best_playlists_id=[]
        for playlist_id in sorted_playlist_dict:
            best_playlists_id.append(str(playlist_id))
            best_match_playlist.append(self.df_playlist_id[self.df_playlist_id['pid'] == int(playlist_id)]['track_uri'].item().split(';'))
        self.best_playlists = best_playlists_id
        best_match_playlists_song_uris_flatlist = [i for b in map(lambda x: [x] if not isinstance(x, list) else x, best_match_playlist) for i in b]
          # stores all the songs of the 5 best playlists
        res = sorted(set(best_match_playlists_song_uris_flatlist), key=lambda x: best_match_playlists_song_uris_flatlist.count(x),
                     reverse=True)  # sort songs_urls based on how many times the song appears in the 5 best playlists
        res = [x for x in res if x not in self.input_song_uris]  # remove the songs from the original playlist
        output_song_uris = res[:sample_size]  # get the n best songs that will be recommended
        songs_occurences = []
        for i in output_song_uris:
            songs_occurences.append(best_match_playlists_song_uris_flatlist.count(i))
        return output_song_uris, songs_occurences


    def generate_explanation(self):
        explanation = ""
        explanation = explanation + "Your input playlist has songs that appear in {} playlists in " \
                                    "our dataset.\n".format(len(set(self.song_searcher())))
        explanation = explanation + "I chose to recommend songs to you from the playlists that match yours best.\n" \
                                    "Among your 5 best matches users that added songs like yours to their playlist also added these:\n"

        return explanation

    def generate_group_explanation(self):
        explanation = ""
        explanation = explanation + "Your input playlists have songs that appear in {} playlists in our " \
                                    "dataset.\n".format(len(set(self.song_searcher())))
        explanation = explanation + "I joined your playlists and recommended songs to you from playlists " \
                                    "that match your playlist combination best.\n" \
                                    "Among the 5 best matches of the combined playlist, " \
                                    "people who added songs like yours to their playlist also added these:\n"
        return explanation
