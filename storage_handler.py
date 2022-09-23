from os.path import basename, dirname, abspath, join, exists, relpath, isfile
from os import makedirs, getenv, listdir
import re
import logging
import sys
from datetime import date, datetime
import pandas as pd
from enum import Enum
# Windows path fix, if system is windows then it replaces the forward slashes for the regex statement later
"""
Purpose of script:
a)  Define directory paths
"""
class Type(Enum):
    PLAYLIST = 1
    SONG = 2
# local data folder structure
DIR_ROOT = dirname(abspath(__file__))
DIR_DATA = join(DIR_ROOT, 'data')
DIR_DATA_JSON=join(DIR_DATA,'json')
DIR_DATA_CSV=join(DIR_DATA,'csv')

CSV_PLAYLISTS=join(DIR_DATA_CSV,"playlists.csv")
CSV_SONGS=join(DIR_DATA_CSV,"songs.csv")

PLAYLIST_COLUMNS=["name",
        "collaborative",
        "pid",
        "modified_at",
        "num_albums",
        "num_tracks",
        "num_followers",
        "num_edits",
        "duration_ms",
        "num_artists",
        "description",
        "tracks"
]
SONGS_COLUMNS=[
        "pos",
        "artist_name",
        "artist_uri",
        "album_uri",
        "album_name",
        "track_uri",
        "track_name",
        "duration_ms",
]
class Storage:
    def __init__(self):

        self._setup()

    def _setup(self):
        # create local data folder structure, if it doesn't exist yet
        for d in [DIR_DATA,DIR_DATA_JSON,DIR_DATA_CSV]:
            makedirs(d, exist_ok=True)
        print('Storage set up.')
        self._setup_csv()
    def _give_empty_df(self,columns):
        return pd.DataFrame(columns=columns)
    def _setup_csv(self):
        if not exists(CSV_PLAYLISTS):
                df = self._give_empty_df(PLAYLIST_COLUMNS)
                df.to_csv(CSV_PLAYLISTS, index=False)
        if not exists(CSV_SONGS):
            df = self._give_empty_df(SONGS_COLUMNS)
            df.to_csv(CSV_SONGS, index=False)
    def add_item(self, type, row):
        if type == Type.PLAYLIST:
            filepath=CSV_PLAYLISTS
            df = read_csv(filepath)
            pid=int(row[2])
            column = df['pid'].values
            if pid in column:
                print(f"Duplicate playlist detected ( with {pid}   as pid)  , not adding to dataframe")
            else:
                new_row = pd.DataFrame([row], columns=PLAYLIST_COLUMNS)
                df = pd.concat([df, new_row])
                df.to_csv(filepath, index=False)
        if type == Type.SONG:
            filepath = CSV_SONGS
            df = read_csv(filepath)
            uri = str(row[5])
            column = df['track_uri'].values
            if uri in column:
                print("Duplicate song detected, not adding to dataframe")
            else:
                new_row = pd.DataFrame([row], columns=SONGS_COLUMNS)
                df = pd.concat([df, new_row])
                df.to_csv(filepath, index=False)

def read_csv(file_path):
    try:
        data = pd.read_csv(file_path, sep=",", encoding='utf-8')
        # print(data)
        return data
    except Exception:
        print("Something went wrong when trying to open the csv file!")
        sys.exit(2)
