import random

def song_searcher(input_song_uris, df_songuri):
    playlist_id_collection = []
    for uri in input_song_uris:  # this loop is run 5 times
        playlist_id_collection.append(df_songuri.get(uri))

    flat_list = [i for b in map(lambda x:[x] if not isinstance(x, list) else x, playlist_id_collection) for i in b]
    separated_list = []
    for element in flat_list:
        separated_list.append(element.split(';'))

    separated_list = [i for b in map(lambda x:[x] if not isinstance(x, list) else x, separated_list) for i in b]
    return separated_list

def playlist_counter(separated_list):
    playlist_dictionary = dict(
        (playlist_id, separated_list.count(playlist_id)) for playlist_id in set(separated_list))
    sorted_playlist_dict = {key: val for key, val in sorted(playlist_dictionary.items(), key=lambda ele: ele[1], reverse=True)}
    return sorted_playlist_dict


def song_suggester(sorted_playlist_dict, sample_size, df_pl_id):
    best_match_playlist = df_pl_id.iat[int(list(sorted_playlist_dict.keys())[0]), 1]
    best_match_playlist_list = best_match_playlist.split(';')
    output_song_uris = random.sample(best_match_playlist_list, k=sample_size)
    return output_song_uris
