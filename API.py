import spotipy
#Authentication - without user
from spotipy import SpotifyClientCredentials

if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials(client_id='61411c9b9d0d416c984da1fb3515ffd4', client_secret='707610ca81b94e6cb4e1b4f3c093f78b')
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    playlist_link = "https://open.spotify.com/playlist/7tRfOpEVloAasjdGg6yVOy?si=svCB_QjJR_a_62MW0b7Kzg"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

    for track in sp.playlist_tracks(playlist_URI)["items"]:
        # URI
        track_uri = track["track"]["uri"]

        # Track name
        track_name = track["track"]["name"]
        print(track_name)
