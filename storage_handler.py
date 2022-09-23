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

PLAYLIST_COLUMNS=["name",
        "collaborative",
        "pid",
        "num_albums",
        "num_tracks",
        "num_followers",
        "num_edits",
        "num_artists"
]
SONGS_COLUMNS=[
        "artist_name",
        "album_name",
        "track_uri",
]
DATAFRAME_COLUMNS=PLAYLIST_COLUMNS+SONGS_COLUMNS
print(DATAFRAME_COLUMNS)
class Storage:
    def __init__(self):

        self._setup()
        self.df=read_csv(CSV_PLAYLISTS)
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
                df = self._give_empty_df(DATAFRAME_COLUMNS)
                df.to_csv(CSV_PLAYLISTS, index=False)
    def add_item(self,  row):
        filepath=CSV_PLAYLISTS
        pid=int(row[2])
        column = self.df['pid'].values
        if pid in column:
            print(f"Duplicate playlist detected ( with {pid}   as pid)  , not adding to dataframe")
        else:
            new_row = pd.DataFrame([row], columns=DATAFRAME_COLUMNS)
            self.df = pd.concat([self.df, new_row])
    def save_data(self):
        self.df.to_csv(CSV_PLAYLISTS, index=False)
def read_csv(file_path):
    try:
        data = pd.read_csv(file_path, sep=",", encoding='utf-8')
        # print(data)
        return data
    except Exception:
        print("Something went wrong when trying to open the csv file!")
        sys.exit(2)
