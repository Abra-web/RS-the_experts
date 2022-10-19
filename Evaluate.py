import math
import numpy as np
import spotipy

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import precision_recall_fscore_support
from spotipy.oauth2 import SpotifyClientCredentials
from numpy import dot
from numpy.linalg import norm
from sklearn.metrics import ndcg_score
from sklearn import preprocessing


class Evaluate:
    def __init__(self, playlist):  # assuming playlist is a list of song urls
        self.playlist = playlist
        # Authentication - without user
        cid = "06c57b85db524a1094cf9a9e3258b68c"
        secret = "a1714a109e3542fa81a7c4c6da457fb8"
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_accuracy_of_ranks(self, recommendations):
        recommended_rank = {}
        # with this loop we acquire new rank to compare with other rank (the recommended list)
        for recommendation in recommendations:
            recommended_rank[recommendation] = self.get_relevance_score(recommendation)

        ideal_rank = {k: v for k, v in sorted(recommended_rank.items(), key=lambda item: item[1])} # sorting to get idealized rank
        return ideal_rank, recommended_rank

    # takes the recommended song, goes through the whole playlist and gets a relevance score of playlist <-> recommended song
    def get_relevance_score(self, songURL):
        final_values = []
        data_of_recommended = self.get_song_values(songURL)
        # normalizing loudness
        data_of_recommended[1] = (data_of_recommended[1] - (-60)) / (0 - (-60))
        # get cosine similarity of the song to each song in the playlist one by one. In the end normalize according to playlist size
        for song in self.playlist:
            data_of_song = self.get_song_values(song)
            # normalizing loudness
            data_of_song[1] = (data_of_song[1] - (-60)) / (0 - (-60))

            # for debug
            # print("Data of song")
            # print(data_of_song)
            # print("Data of recommended")
            # print(data_of_recommended)
            # print("Similarity values")
            # print(dot(data_of_recommended, data_of_song) / (norm(data_of_recommended) * norm(data_of_song)))
            final_values.append(dot(data_of_recommended, data_of_song) / (norm(data_of_recommended) * norm(data_of_song)))  # returns a value at most 1
            # print("")

        # print("")
        # print("")
        # testing
        # print("Old")
        # print("Final values:")
        # print(final_values)
        # print("Normally")
        # temp_final_value = sum(final_values) / len(self.playlist)
        # print(temp_final_value)
        # final_values = preprocessing.normalize([final_values])  # normalize list
        # print("New")
        # print("New final values:")
        # print(final_values)
        # print("Actually")
        # final_value = sum(final_values[0]) / len(self.playlist)  # get final score
        # print(final_value)
        final_values = preprocessing.normalize([final_values])
        # print(final_values)
        final_value = sum(final_values[0]) / len(final_values[0])
        # print(final_values[0])
        # print(final_value)
        return final_value

    def get_song_values(self, songURL):
        data_of_recommended_dict = self.sp.audio_features(songURL)[0]

        # since we will get dict, turn it into list (which is only a song) so that we can use it for cosine similarity
        data_of_recommended_list = list(data_of_recommended_dict.values())
        # form the dict we need; [0:1], [3], [5:10]
        a, b, c = data_of_recommended_list[0:1], [data_of_recommended_list[3]], data_of_recommended_list[5:10]
        return a + b + c

    # main function here
    def calculate_nDCG(self, recommendations):
        new_ideal_rank, new_recommended_rank = self.get_accuracy_of_ranks(recommendations)

        ideal_values = list(new_ideal_rank.values())
        # not sure if this is right, but I think changing the final values into integers sorted by increasing vals
        # makes us give more legit result
        recommended_values = self.replace_val(list(new_recommended_rank.values()))

        nDCG = ndcg_score(np.asarray([self.replace_val(ideal_values)]), np.asarray([recommended_values]))
        # print("Recommended rank")
        # print(recommended_values)
        # print("Ideal")
        # print(ideal_values)
        avg_to_playlist = sum(list(new_recommended_rank.values())) / len(new_recommended_rank)
        return nDCG, avg_to_playlist, list(new_recommended_rank.values())

    def replace_val(self, given_list):
        temp = given_list
        current_smallest = 1
        i = 1
        for x in range(0, len(temp)):
            for y in temp:
                if y < current_smallest:
                    current_smallest = y

            index = temp.index(current_smallest)
            temp[index] = i
            i += 1
            current_smallest = 1

        return temp

    def swap_val(self, given_list):
        temp = given_list
        a = len(given_list) - 1
        for x in range(0, int(len(given_list) / 2)):
            temp[x], temp[a] = temp[a], temp[x]
            a -= 1

        return temp


