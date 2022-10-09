import math
import numpy as np
#import spotipy # TODO

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import precision_recall_fscore_support
#from spotipy.oauth2 import SpotifyClientCredentials
from numpy import dot
from numpy.linalg import norm
from sklearn.metrics import ndcg_score

# for testing purposes
#if __name__ == '__main__':
#    # pull the data from the files
#    the_playlist = ["id1", "id2", "id3", "id4", "id5"]
#    assumed_recommended_list =


class Evaluate:
    def __init__(self, playlist): # assuming playlist is a list of song urls
        self.playlist = playlist

    def get_accuracy_of_ranks(self, playlist, recommendations):
        recommended_rank = {}
        # with this loop we acquire new rank to compare with other rank (the recommended list)
        for recommendation in recommendations:
            recommended_rank[recommendation] = self.get_relevance_score(playlist, recommendation)

        ideal_rank = {k: v for k, v in sorted(recommended_rank.items(), key=lambda item: item[1])} # sorting to get idealized rank
        return ideal_rank, recommended_rank

    # takes the recommended song, goes through the whole playlist and gets a relevance score of playlist <-> recommended song
    def get_relevance_score(self, playlist, songURL):
        final_value = 0
        data_of_recommended = self.get_song_values(songURL)
        # get cosine similarity of the song to each song in the playlist one by one. In the end normalize according to playlist size
        for song in playlist:
            data_of_song = self.get_song_values(song)
            final_value += dot(data_of_recommended, data_of_song) / (norm(data_of_recommended) * norm(data_of_song)) # returns a value at most 1

        return final_value / len(playlist) # normalize to 0-1

    def get_song_values(self, songURL):
        data_of_recommended_dict = audio_features(songURL) # TODO here we assume we get the values as a dict

        # since we will get dict, turn it into list (which is only a song) so that we can use it for cosine similarity
        data_of_recommended_list = list(data_of_recommended_dict.values())
        # form the dict we need; [0:1], [3], [5:10]
        a, b, c = data_of_recommended_list[0:1], data_of_recommended_list[3], data_of_recommended_list[5:10]
        return a + b + c

    # defining hits, lower the hit benchmark depending on the size of the playlist
    def calculate_nDCG(self, playlist, recommendations):
        new_ideal_rank, new_recommended_rank = self.get_accuracy_of_ranks(playlist, recommendations)
        nDCG = ndcg_score(new_ideal_rank.values(), new_recommended_rank.values())
        return nDCG









    """ 
    -----TRASH----
    This method defines our methodology;
    In the end, it will return us a new df "itemID | songURL | Relevant"
    
    How we compute the relevance for each song?
    - I suppose what we can do here is that for every recommended song we will go through all the songs the playlist 
    contains (so like "user's preferences") and see how much the values of "'danceability', 'energy', ..." differ
    If addition of difference is >1 give 0 for relevance, else 1 (this part can be changed; TODO)
    
    :param playlist: The playlist that we tried to recommend to
    :param recommendations: The recommendations the playlist got
    def get_user_rated_movies_plots(self, playlist, recommendations):

        playlist  # select the ratings of the user
        rated_movies_df = movies_df.loc[
            list(playlist['item'])]  # select the movie information for the movies rated by the user
        rated_movies_df = rated_movies_df[['title', 'plot']]  # select only the information we need
        playlist = playlist.set_index('item')  # set the index for the next join
        rated_movies_df = rated_movies_df.join(playlist['rating'], on='item')  # join the two dataframes
        rated_movies_df['relevant'] = rated_movies_df['rating'].apply(
            lambda x: 1 if x > 3 else 0)  # compute the relevance values for the user
        return rated_movies_df

# I need the playlist, the songs it contains, and data about it
    def creating_test_training_set_with_kFold(self):
        user_plots_ratings_df = get_user_rated_movies_plots(user, ratings_df,
                                                            movies_df)  # retrieve user info with the previously defined method

        X_plots = user_plots_ratings_df['plot']  # select the Plot column, from which we will compute ourTF-IDF features
        y = user_plots_ratings_df['relevant']  # select the elevant column, that will be used as label

        kf = KFold()
        X_plots_train, X_plots_test, y_train, y_test = train_test_split(X_plots, y,
                                                                        test_size=0.2)  # randomly splits the data in train and test, we specify that 20% of the data will go into the test set

        vectorizer = TfidfVectorizer()
        X_train = vectorizer.fit_transform(X_plots_train)  # Trains our TF-IDF model and computes the features

        neigh = KNeighborsClassifier(n_neighbors=10)
        neigh.fit(X_train, y_train)  # train our cassifier

        X_test = vectorizer.transform(X_plots_test)
        y_pred = neigh.predict(X_test)  # evaluates the predictions of the classifier

        return precision_recall_fscore_support(y_test, y_pred, average="binary",
                                               zero_division=0)  # compare the real relevance values with the predicted one, and return precision, recall, and fscore
        """

