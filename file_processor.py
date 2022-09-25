from storage_handler import Storage,join, DIR_DATA_JSON,Type,SONGS_COLUMNS,PLAYLIST_COLUMNS,read_csv
import glob,json
import sys, time

def process_all(storage):
    json_files = glob.glob(join(DIR_DATA_JSON, "*.json"))
    count=0
    for files in json_files:
        f = open(files)
        js = f.read()
        f.close()
        slice = json.loads(js)
        for playlist in slice["playlists"]:
            process_playlist(playlist,storage)
            count += 1
            if count % 100 == 0:
                print(f"Processed {count} playlists!")
        storage.save_data()
def process_playlist(playlist,storage):
    playlist_row=list()
    for fields in PLAYLIST_COLUMNS:
        playlist_row.append(str(playlist[fields]))
    tracks=playlist["tracks"]
    tracks_list=set()
    artists_list=set()
    album_list=set()
    for dicts in tracks:
        tracks_list.add(dicts['track_uri'])
        artists_list.add(dicts['album_name'])
        album_list.add(dicts['artist_name'])
    playlist_row.append(";".join(artists_list))
    playlist_row.append(";".join(album_list))
    playlist_row.append(";".join(tracks_list))
    storage.add_item(playlist_row)
def process_songs(songs):
    for song in songs:
        song_row=list()
        for fields in SONGS_COLUMNS:
            song_row.append(str(song[fields]))
        storage.add_item(Type.SONG,song_row)

if __name__ == '__main__':
    storage = Storage()
    json_files=glob.glob(join(DIR_DATA_JSON,"*.json"))
    start: float = time.time()
    print("STARTING TRANSFORMATION OF JSON FILES")
    f = open(json_files[0])
    js = f.read()
    f.close()
    slice = json.loads(js)
    # process_playlist(slice["info"])
    count = 0
    for playlist in slice["playlists"]:
        process_playlist(playlist)
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} playlists!")
    end = time.time()
    storage.save_data()
    print("\n--- DONE ---")
    print("Time taken: ", time.strftime('%H:%M:%S', time.gmtime(end - start)))

