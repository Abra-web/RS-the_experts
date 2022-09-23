from storage_handler import Storage,join, DIR_DATA_JSON,Type,SONGS_COLUMNS,PLAYLIST_COLUMNS
import glob,json
import sys, time

def process_all():
    storage = Storage()
    json_files = glob.glob(join(DIR_DATA_JSON, "*.json"))
    for files in json_files:
        f = open(files)
        js = f.read()
        f.close()
        slice = json.loads(js)
        process_playlist(slice["info"])
        for playlist in slice["playlists"]:
            process_playlist(playlist)
def process_playlist(playlist):
    playlist_row=list()
    for fields in PLAYLIST_COLUMNS:
        if fields == "description":
            try:
                playlist_row.append(playlist[fields])
            except:
                playlist_row.append("")
        elif fields !="tracks": # Tracks always last
            playlist_row.append(str(playlist[fields]))
    tracks=playlist["tracks"]
    process_songs(tracks)
    tracks_list=list()
    for dicts in tracks:
        tracks_list.append(dicts['track_uri'])
    playlist_row.append(";".join(tracks_list))
    storage.add_item(Type.PLAYLIST,playlist_row)
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
    print("\n--- DONE ---")
    print("Time taken: ", time.strftime('%H:%M:%S', time.gmtime(end - start)))

