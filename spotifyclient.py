import json, requests
from track_playlist import Track, Playlist

#This class will perform operations with Spotify API
class SpotifyClient:
    #Constructor
    def __init__(self, auth_token, user_id):
        """
        :param authorization_token (str): API token
        :param user_id (int): Spotify user ID
        """
        self.auth_token = auth_token
        self.user_id = user_id

    def get_recent_tracks(self, limit =10):
        """
        :param limit (int): Number of last played songs to get, default is 10
        :return tracks (list of Tracks): Last played songs
        """
        #Formats our api url
        url = "https://api.spotify.com/v1/me/player/recently-played?limit=" + str(limit)
        #Calls function that will request the API (using another method that utilizes the auth token)
        #We call the method with self.methodName because the method is part of this class (self)
        response = self._place_get_api_request(url)
        #Then, we must 'convert' this request to json, so that it's a python dictinonary of data for tracks
        response_json = response.json()
        #Now, we retrieve the last played tracks by looping through this JSON dictionary
        #We loop through response_json's items and call the Track() constructor to pass values 
        #using multiple key indexes since the JSON dictionary is nested
        #Ex: The artist's "name" value is nested so we access "track", then "artist" then "0", then "name"
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) 
        for track in response_json["items"]]
        #Finally, we return this list of tracks (a list of Track objects)
        return tracks

    def get_recs(self, ref_tracks, limit=50):
        """
        :param ref_tracks (list) : Seed tracks (inputted by user), less than 5
        :param limit: Number of tracks to recommend
        :return tracks (list of Tracks): Recommended songs
        """
        ref_tracks_url = ""
        #Here, we'll loop through the list of reference tracks and append the url segment with track IDs
        for ref_track in ref_tracks:
            ref_tracks_url += ref_track.id + ","
        #Our last track ID ended with a ',', so we remove the last character of the string
        ref_tracks_url = ref_tracks_url[:-1]
        url = "https://api.spotify.com/v1/recommendations?seed_tracks=" + ref_tracks_url + "&limit=" + str(limit)
        #Again, we request the API, but this time, using the ref tracks, get the data for recommended tracks
        response = self._place_get_api_request(url)
        response_json = response.json()
        #Again, we make a list of track objects using the JSON data from the reccomended tracks, but with 
        #slightly different, simplifer indexes
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) 
        for track in response_json["tracks"]]
        #Finally, return the recommended tracks
        return tracks
    
    #This method is used for getting data from the API (mainly for track retrieval)
    #The underscore before the method name means that this method is meant to be called IN THIS class itself
    def _place_get_api_request(self,url):
        #We call the request for JSON content, and pass in our authorization token as a header in the correct
        #format that the API uses, we also include Content-Type header since we're retrieving JSON text
        response = requests.get(url, headers = {"Authorization": "Bearer " + self.auth_token,\
                                                "Content-Type":"application/json"})
        #Response holds the data, and can be interpreted as a dictionary when we convert to JSON
        return response
    
    def create_playlist(self, name):
        """
        :param name (Str): Name of our playlist
        :return playlist (Playlist): The playlist that we create
        """
        #This converts a dictionary to a JSON string, and will be used to send JSON data
        #into the playlist so that it has the approperiate name, description, and privacy type
        playlistDict = {"name": name, "description": "Recommended Songs", "public": True}
        playlistData = json.dumps(playlistDict)
        #Creates URL using the user_id attribute
        url = "https://api.spotify.com/v1/users/" + self.user_id + "/playlists"
        #Calls method to request post API and converts to JSON
        response = self._place_post_api_request(url, playlistData)
        response_json = response.json()
        #Now, we create the actual playlist object, first retrieving the id of the new playlist via JSON string
        playlist_id = response_json['id']
        playlist = Playlist(name, playlist_id)
        #Returns the (currently empty) playlist
        return playlist

    def fill_playlist(self, playlist, tracks):
        """
        :param playlist (Playlist): The playlist we'll fill
        :param tracks (list of Tracks): The tracks we'll put in the playlist
        :return response: API response
        """
        #We have a list of tracks, but need the URIs of each track in a list as well, so we
        #use the create URI method on each track in the list
        tracks_uris = [track.create_uri() for track in tracks]
        #Converts the list to a JSON string so that we can post it to the API with the URL
        playlistData = json.dumps(tracks_uris)
        url = "https://api.spotify.com/v1/playlists/" + playlist.id + "/tracks"
        #Calls method to request post API and converts to JSON 
        response = self._place_post_api_request(url, playlistData)
        response_json = response.json()
        #Finally, we simply return the JSON string itself
        return response_json

    #This method is used to POST data using the API (mainly to createing/populating playlists)
    def _place_post_api_request(self,url, playlistData):
        #Again, we call a request for JSON, but this time use requests.post so we can insert the playlist's 
        #data as a JSON string, using the same headers as well
        response = requests.post(url, data=playlistData, headers = {"Authorization": "Bearer " + self.auth_token, 
                                                "Content-Type":"application/json"})
        #Response holds the data, and can be interpreted as a dictionary when we convert to JSON
        return response