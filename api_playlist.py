import json
from datetime import date

import secret_holder
from secret_holder import spotify_user_id, playlist_id
import requests
from refresh import Refresh


class api_playlist:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.playlist_id = playlist_id
        self.tracks = ""
        self.new_playlist_id = ""

    def find_songs(self):

        # print("Finding songs in playlist...")
        # Loop through playlist tracks, add them to list

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()

        # print(response)

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]

        self.add_to_playlist()

    def create_playlist(self):
        # Create a new playlist
        # print("Trying to create playlist...")
        today = date.today()

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)

        request_body = json.dumps({
            "name": "test", "description": "Test", "public": True
        })

        response = requests.post(query, data=request_body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })

        response_json = response.json()

        return response_json["id"]

    def add_to_playlist(self, tracks):
        # add all songs to new playlist
        # print("Adding songs...")

        self.new_playlist_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.new_playlist_id, tracks)

        response = requests.post(query, headers={"Content-Type": "application/json",
                                                 "Authorization": "Bearer {}".format(self.spotify_token)})

        # print(response.json)

    def call_refresh(self):

        # print("Refreshing token")

        refreshCaller = Refresh()

        self.spotify_token = refreshCaller.refresh()

        #self.find_songs()

    def get_name(self, track_id):
        valid_id = track_id[14:]
        query = "https://api.spotify.com/v1/tracks/{}".format(
            valid_id)

        response = requests.get(query, headers={"Content-Type": "application/json",
                                                 "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()
        #print(response_json)
        return response_json['name'], response_json['artists'][0]['name']


    def get_features(self, track_id):
        valid_id = track_id #track_id[14:]
        query = "https://api.spotify.com/v1/audio-features/{}".format(
            valid_id)

        response = requests.get(query, headers={"Content-Type": "application/json",
                                                "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()
        return response_json

    def get_songs(self, uri):
        # print("Finding songs in playlist...")
        # Loop through playlist tracks, add them to list

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()

        #print(response)

        tracks = ''

        for i in response_json["items"]:
            tracks += (i["track"]["uri"] + ",")
        tracks = tracks[:-1]

        return tracks

if __name__ == '__main__':

    a = api_playlist()
    a.call_refresh()