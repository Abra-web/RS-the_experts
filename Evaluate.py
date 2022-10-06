from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import precision_recall_fscore_support
import numpy as np

class Evaluate:
    def __init__(self, playlist):
        self.playlist = playlist

    # takes the recommended song, goes through the whole playlist adding the differences
    def get_relevance_score(self, playlist, songURL):
        final_value = 0
        data_of_recommended = audio_features(songURL)
        for song in playlist:
            data_of_song = audio_features(song)
            final_value += np.sum(np.subtract(list(data_of_song.values()), list(data_of_recommended.values())))

        return final_value


    def accuracy_of_ranks(self, playlist, recommendations):
        actual_rank = {}
        # with this loop we try to get the actually good list
        for recommendation in recommendations:
            actual_rank[recommendation] = self.get_relevance_score(playlist, recommendation)

        actual_rank_sorted = {k: v for k, v in sorted(actual_rank.items(), key=lambda item: item[1])}









    """ 
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

