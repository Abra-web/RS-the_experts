import csv
import numpy as np

from storage_handler import Storage
from song_searcher import song_searcher
from pytictoc import TicToc
from Evaluate import Evaluate

# because doing addition to float numbers makes it give funny numbers
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


if __name__ == '__main__':
    # loading storage
    t = TicToc()
    t.tic()
    storage = Storage()
    # print("Loading playlists...")
    df_pl_id = storage.give_playlist()
    # print("Loading songs...")
    df_song_uris = storage.give_songs()

    # randomly chosen 30 playlist ids
    playlist_ids = [171076, 325544, 319651, 147028, 22572, 229709, 334088, 370651, 105751, 214920, 126328, 339561,
                    298939, 392705, 149063, 482346, 31093, 353847, 150875, 97545, 73782, 256293, 358731, 353398,
                    223042, 232543, 51005, 7794, 458332, 242101]

    # commenting out this part, because if re-run this code the data will be lost
    # with open('collecting_data.csv', 'w', newline='') as file:
    #     2. Create a CSV writer
        # writer = csv.writer(file)
        # 3. Write data to the file
        # new_data = ["song_id", "list_length", "threshold", "nDCG_val", "avg_to_playlist", "list_of_values"]
        # writer.writerow(new_data)

    final_line = []
    # this method helps to skip the whole file and immediately goes to final line
    with open('collecting_data.csv', "r") as f:
        for line in f: pass
        final_line = list(line.split(","))  # this is the last line of the file; also converting to list

    last_length = int(final_line[1])
    last_thresh = truncate(float(final_line[2]), 3)
    last_playlist_id = int(final_line[0])
    last_playlist_id_index = playlist_ids.index(last_playlist_id)

    # handling additional conditions
    if last_playlist_id_index == (len(playlist_ids) - 1):
        if last_thresh != 0.3:
            last_thresh += truncate(last_thresh + 0.05, 3)
            last_playlist_id_index = -1
        else:
            last_length += 5
            last_thresh = 0.1
            last_playlist_id_index = -1

    for list_length in range(last_length, 25, 5):
        for threshold in np.arange(last_thresh, 0.35, 0.05):
            # had to do this weird loop to be able to start from last playlist id
            for i in range(last_playlist_id_index + 1, len(playlist_ids)):
                threshold = truncate(threshold, 3)
                playlist_id = playlist_ids[i]
                song_strings = df_pl_id[df_pl_id['pid'] == playlist_id]["track_uri"].item()
                song_uris = song_strings.split(';')

                # change params here
                rs = song_searcher(song_uris, df_song_uris, df_pl_id, threshold, list_length)

                output_song_uris = rs.recommend_songs(5)
                temp = Evaluate(song_uris)
                # also saving the list of similarity values; such that if later we need new calculations
                nDCG_val, avg_to_playlist, list_of_values = temp.calculate_nDCG(output_song_uris)

                # 1. Open a new CSV file: Structure of data is: = ['song_id', 'avg', 'nDCG_val', 'list']
                with open('collecting_data.csv', 'a', newline='') as file:
                    # 2. Create a CSV writer
                    writer = csv.writer(file)
                    # 3. Write data to the file
                    new_data = [playlist_id, list_length, threshold, nDCG_val, avg_to_playlist, list_of_values]
                    writer.writerow(new_data)

                # handling additional conditions (resetting index and thresh values)
                if last_playlist_id_index == (len(playlist_ids) - 1):
                    if last_thresh == 0.3:
                        last_thresh = 0.1

                    last_playlist_id_index = -1  # need to reset index either way

