import pandas as pd

data_set_sorted_by_songuri = pd.read_csv("OURFILELOCATION")
data_set_sorted_by_playlist_id = pd.read_csv("OURFILELOCATION")


def song_searcher(input_song_uris):
    playlist_id_collection = []
    data_su_column_song_uri = data_set_sorted_by_songuri[["track_uri"]]
    data_su_column_playlist_id = data_set_sorted_by_songuri[["playlist_id"]]

    for uri in input_song_uris:  # this loop is run 5 times
        for song in data_su_column_song_uri:  # this loop is run as many times as there are songs
            if song == uri:
                playlist_id = data_su_column_playlist_id[song]
                playlist_id_collection.append(playlist_id)

    return playlist_id_collection


def type_preparer():
    return 0
    # to be written when data is available

def playlist_counter(playlist_id_collection):
    playlist_dictionary = dict(
        (playlist_id, playlist_id_collection.count(playlist_id)) for playlist_id in set(playlist_id_collection))
    key_of_max_value = max(playlist_dictionary, key=playlist_dictionary.get)
    return key_of_max_value


def random_picker(key_of_max_value):
    data_pl_column_playlist_id = data_set_sorted_by_playlist_id[["playlist_id"]]
    for playlist_id in data_pl_column_playlist_id:
        if playlist_id == key_of_max_value:
            return False