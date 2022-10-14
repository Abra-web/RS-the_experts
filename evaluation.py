import numpy as np
import spotipy
from numpy import dot
from numpy.linalg import norm
from sklearn.metrics import ndcg_score
from spotipy.oauth2 import SpotifyClientCredentials


class Evaluate:

    def __init__(self, playlist, recommendations):  # assuming playlist is a list of song urls
        self.playlist = playlist
        self.recommendations = recommendations
        # Authentication - without user
        cid = "06c57b85db524a1094cf9a9e3258b68c"
        secret = "a1714a109e3542fa81a7c4c6da457fb8"
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def give(self):
        cal = self.calculate_nDCG()
        return cal

    def get_accuracy_of_ranks(self):
        recommended_rank = {}
        # with this loop we acquire new rank to compare with other rank (the recommended list)
        for recommendation in self.recommendations:
            recommended_rank[recommendation] = self.get_relevance_score(recommendation)

        ideal_rank = {k: v for k, v in
                      sorted(recommended_rank.items(), key=lambda item: item[1])}  # sorting to get idealized rank
        return ideal_rank, recommended_rank

    # takes the recommended song, goes through the whole playlist and gets a relevance score of playlist <-> recommended song
    def get_relevance_score(self, songURL):
        final_value = 0
        data_of_recommended = self.get_song_values(songURL)
        # get cosine similarity of the song to each song in the playlist one by one. In the end normalize according to playlist size
        for song in self.playlist:
            data_of_song = self.get_song_values(song)
            final_value += dot(data_of_recommended, data_of_song) / (
                        norm(data_of_recommended) * norm(data_of_song))  # returns a value at most 1

        return final_value/len(self.playlist)  # normalize to 0-1

    def get_song_values(self, songURL):
        data_of_recommended_dict = self.sp.audio_features(songURL)[0]

        # since we will get dict, turn it into list (which is only a song) so that we can use it for cosine similarity
        data_of_recommended_list = list(data_of_recommended_dict.values())
        # form the dict we need; [0:1], [3], [5:10]
        a, b, c = data_of_recommended_list[0:1], [data_of_recommended_list[3]], data_of_recommended_list[5:10]
        return a + b + c

    # defining hits, lower the hit benchmark depending on the size of the playlist
    def calculate_nDCG(self):
        new_ideal_rank, new_recommended_rank = self.get_accuracy_of_ranks()
        nDCG = ndcg_score(np.asarray([list(new_ideal_rank.values())]),
                          np.asarray([list(new_recommended_rank.values())]))
        return nDCG