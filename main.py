from song_searcher import song_searcher
import pandas as pd
import os.path
from pathlib import Path

from api_playlist import api_playlist

if __name__ == '__main__':
    # home would contain something like "/Users/jame"
    home = str(Path.home())
    # pull the data from the files
    data_set_sorted_by_song_uri = pd.read_csv(
        home+"\\PycharmProjects\\RS-the_experts\\data\\csv\\songs.csv")
    df_song_uris = pd.DataFrame(data_set_sorted_by_song_uri)
    # transform the dataset to a dict for simple lookup operation (hashtable)
    df_song_uris = df_song_uris.set_index('songs').T.to_dict('list')

    # pull dataframe from files
    data_set_sorted_by_playlist_id = pd.read_csv(
        home+"\\PycharmProjects\\RS-the_experts\\data\\csv\\playlists_extract_pid_sort.csv")
    df_pl_id = pd.DataFrame(data_set_sorted_by_playlist_id)
    # extract only the following columns from dataset cus the rest is not necessary
    df_pl_id = df_pl_id[['pid', 'track_uri']]

    # input data, hopefully soon connected to spotify API
    input_song_uris = ['spotify:track:7H6ev70Weq6DdpZyyTmUXk',
                       'spotify:track:5Q0Nhxo0l2bP3pNjpGJwV1',
                       'spotify:track:1Slwb6dOYkBlWal1PGtnNg',
                       'spotify:track:4VrWlk8IQxevMvERoX08iC',
                       'spotify:track:69bp2EbF7Q2rqc5N3ylezZ']

    # execute functions from song_searcher file (commented there)
    rs = song_searcher(input_song_uris , df_song_uris, df_pl_id)
    output_song_uris = rs.recommend_songs()

    #a = api_playlist()
    #a.call_refresh()
    tracks =''
    for element in output_song_uris:
        tracks += element+","
    tracks = tracks[:-1]

    # print output, hopefully soon connected to Spotify API to add to our playlist
    #print(output_song_uris)
    #a.add_to_playlist(tracks)
    #print(a.get_name('spotify:track:7H6ev70Weq6DdpZyyTmUXk'))
    #print(a.get_features('6Sy9BUbgFse0n0LPA5lwy5'))
    #print(a.get_me())

