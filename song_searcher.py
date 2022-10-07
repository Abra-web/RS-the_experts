import random

class song_searcher:

    def __init__(self, input_song_uris, df_song_uri):
        self.input_song_uris = input_song_uris
        self.df_song_uri = df_song_uri

    #  looks up song ids and returns the playlist ids of all songs (not unique yet)
    def song_searcher(self):
        #  retrieve all playlist id collections based on song_uri
        playlist_id_collection = [] # saves all the playlists the songs occur in
        songs_error = []
        for uri in self.input_song_uris:
            try:
                playlist_id_collection.append(self.df_song_uri.get(uri))
            except:
                songs_error.append(uri)
                print('song was not in our database')


        #  flatten the nested playlist collection list, removes double values??
        flat_list = [i for b in map(lambda x:[x] if not isinstance(x, list) else x, playlist_id_collection) for i in b]

        #  extract the playlist ids out of every playlist collection
        separated_list = []
        for element in flat_list:
            separated_list.append(element.split(';'))

        # flatten created nested list again to get ['id1', 'id2', ...]
        separated_list = [i for b in map(lambda x:[x] if not isinstance(x, list) else x, separated_list) for i in b]
        return separated_list


    #  calculate how many times a playlist appears in the playlist id list
    def playlist_counter(separated_list):
        #  make a dictionary where (key = playlist id) and (value = #of times the id appears in separated list)
        playlist_dictionary = dict(
            (playlist_id, separated_list.count(playlist_id)) for playlist_id in set(separated_list))
        # sort the dictionary by value -> the largest first
        sorted_playlist_dict = {key: val for key, val in sorted(playlist_dictionary.items(), key=lambda ele: ele[1], reverse=True)}
        return sorted_playlist_dict


    # input the number of songs you want out and the key value pairs of id/# and the dataset sorted by playlists
    # outputs the specified number of song uris you want
    def song_suggester(sorted_playlist_dict, sample_size, df_pl_id):
        # retrieve the best matching playlist (string of all song uris), by extracting the first key of the dictionary
        # conversion to int since the id is stored as eg "99".
        best_match_playlist = df_pl_id.iat[int(list(sorted_playlist_dict.keys())[0]), 1]
        # separate song_uris via the ";" delimiter
        best_match_playlist_list = best_match_playlist.split(';')
        #  select a random sample of songs (the algorithm can be improved here if necessary)
        output_song_uris = random.sample(best_match_playlist_list, k=sample_size)
        return output_song_uris
