import sys
import pandas as pd
columns=["name","pid","num_albums","num_tracks","num_followers","num_edits","num_artists","artist_name","album_name","track_uri"] #"collaborative",
columns.remove("pid")
columns.remove("track_uri")

def extract_rows(path, number,outpath):
    try:
        data=read_csv(path)
        output = data[:number]
        output.to_csv(outpath,index=False)
        print("extraction successful")
    except:
        print(f"The file does not have {number} entries, returning entire file.")
def read_csv(file_path):
    try:
        data = pd.read_csv(file_path, sep=",", encoding='utf-8')
        return data
    except Exception:
        print("Something went wrong when trying to open the csv file!")
        sys.exit(2)
def sort(df_path,column):
    df = read_csv(df_path)
    df2=df.sort_values(by=column)
    df2.to_csv(df_path.replace(".csv",f"_{column}_sort.csv"),index=False)


def drop_columns(data):
    columns_to_drop = columns
    try:
        data = data.drop(columns_to_drop,axis=1)
    except Exception:
        print("Something went wrong")
    data.reset_index(inplace=True, drop=True)
    return data

def make_songs_df(path):
    df=read_csv(path)
    pid=df['pid']
    tracks=df['track_uri']
    mapping=dict()
    for i in range(len(pid)):
        playlist=pid[i]
        track=tracks[i]
        track=track.split(sep=";")
        for t in track:
            if t in mapping:
                mapping[t]=mapping[t]+";"+str(playlist)
            else:
                mapping[t]=str(playlist)
    return mapping