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

    # defining hits, lower the hit benchmark depending on the size of the playlist
    def calculate_nDCG(self):
        new_ideal_rank, new_recommended_rank = self.get_accuracy_of_ranks()
        nDCG = ndcg_score(np.asarray([list(new_ideal_rank.values())]),
                          np.asarray([list(new_recommended_rank.values())]))
        return nDCG