from storage_handler import Storage
from song_searcher import song_searcher
from pytictoc import TicToc
from api_playlist import api_playlist

if __name__ == '__main__':
    t = TicToc()
    t.tic()
    storage = Storage()
    print("Loading playlists...")
    df_pl_id = storage.give_playlist()
    print("Loading songs...")
    df_song_uris = storage.give_songs()
    playlist_id = int(input('Which playlist would you like to recommend songs to?'))
    print('input received. Getting playlist...')
    song_strings = df_pl_id[df_pl_id['pid'] == playlist_id]["track_uri"].item()
    print('input received. Prepping playlist for use...')
    song_uris = song_strings.split(';')
    print('Playlist has length: '+ str(len(song_uris)))
    print("recommending songs and exiting main...")
    # execute functions from song_searcher file (commented there)
    rs = song_searcher(song_uris, df_song_uris, df_pl_id,0.2,10)

    print("found songs...")
    output_song_uris = rs.recommend_songs(5)

    a = api_playlist()
    a.call_refresh()
    tracks =''
    for element in output_song_uris:
        tracks += element+","
    for element in song_uris:
        tracks += element+","
    tracks = tracks[:-1]
    t.toc()
    #a.add_to_playlist(tracks)
    for b in output_song_uris:
        print(a.get_name(b))


