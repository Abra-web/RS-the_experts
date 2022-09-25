from os.path import dirname, abspath, join, exists
from os import makedirs
import sys
import pandas as pd
from enum import Enum
from csv_extractor import extract_rows,read_csv,sort
"""
Purpose of script:
a)  Define directory paths
"""
class Type(Enum):
    MAIN = 1
    EXTRACT = 2
# local data folder structure
DIR_ROOT = dirname(abspath(__file__))
DIR_DATA = join(DIR_ROOT, 'data')
DIR_DATA_JSON=join(DIR_DATA,'json')
DIR_DATA_CSV=join(DIR_DATA,'csv')

CSV_PLAYLISTS=join(DIR_DATA_CSV,"playlists.csv")
CSV_PLAYLISTS_EXTRACT=CSV_PLAYLISTS.replace(".csv","_extract.csv")
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
class Storage:
    def __init__(self):
        self._setup()
        self.df=read_csv(CSV_PLAYLISTS)
        print("data loaded")
    def _setup(self):
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
    def extract(self,number):
        extract_rows(CSV_PLAYLISTS,number,CSV_PLAYLISTS_EXTRACT)
    def add_item(self,  row):
        pid=int(row[2])
        column = self.df['pid'].values
        if pid in column:
            print(f"Duplicate playlist detected ( with {pid}   as pid)  , not adding to dataframe")
        else:
            new_row = pd.DataFrame([row], columns=DATAFRAME_COLUMNS)
            self.df = pd.concat([self.df, new_row])
    def save_data(self):
        self.df.to_csv(CSV_PLAYLISTS, index=False)
    def sort(self,df_type,column):
        if df_type == Type.MAIN:
            sort(CSV_PLAYLISTS,column)
        elif df_type == Type.EXTRACT:
            sort(CSV_PLAYLISTS_EXTRACT, column)