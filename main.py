import song_searcher as ss
import pandas as pd

if __name__ == '__main__':
    songURLs = pd.read_csv(
        "C:\\Users\\Tabea Heusel\\PycharmProjects\\RS-the_experts\\data\\csv\\songs.csv")
    df_songURLs = pd.DataFrame(songURLs)
    df_songURLs = df_songURLs.set_index('songs').T.to_dict('list')

    playlistIDs = pd.read_csv(
        "C:\\Users\\Tabea Heusel\\PycharmProjects\\RS-the_experts\\data\\csv\\playlists_extract_pid_sort.csv")
    df_playlistIDs = pd.DataFrame(playlistIDs)
    df_playlistIDs = df_playlistIDs[['pid', 'track_uri']]

    input_song_URLs = ['spotify:track:7H6ev70Weq6DdpZyyTmUXk',
                       'spotify:track:5Q0Nhxo0l2bP3pNjpGJwV1',
                       'spotify:track:1Slwb6dOYkBlWal1PGtnNg',
                       'spotify:track:4VrWlk8IQxevMvERoX08iC',
                       'spotify:track:69bp2EbF7Q2rqc5N3ylezZ']

    step1 = ss.song_searcher(input_song_URLs, df_songURLs)
    step2 = ss.playlist_counter(step1)
    step3 = ss.song_suggester(step2, 5, df_playlistIDs)
    print(step3)
