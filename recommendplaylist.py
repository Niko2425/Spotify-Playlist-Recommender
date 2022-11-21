import os 
from spotifyclient import SpotifyClient
#Must set the AUTH_TOKEN and USER_ID before running script
#https://developer.spotify.com/console/post-playlists/
#https://developer.spotify.com/console/get-current-user/

def main():
    #Makes instance of spotifyclient (this will let us import and create all the tracks and playlists)
    #Since the token and user ID are private info, user must manually set environmental vars by typing:
    #set AUTH_TOKEN=(their token), then set USER_ID=(their id)
    spotify_client = SpotifyClient(os.getenv("AUTH_TOKEN"), os.getenv("USER_ID"))

    #Then, retrieve the last played tracks and put into list
    num_tracks_to_fetch = int (input("Hello! How many recent tracks would you like to retrieve: "))
    recent_tracks = spotify_client.get_recent_tracks(num_tracks_to_fetch)
    #Display all the tracks back to user, with indices starting at 1
    track_index = 1
    for track in recent_tracks:
        print(str(track_index) + ": " + track.name + " by " + track.artist + "\n")
        track_index+=1
    #Then, ask user which tracks to pick for the reference in the recommendation
    index_choice = input("Now, choose up to 5 tracks to use as references during the process. "
    "Use the tracks' numerical indicies, separated only by commas: ")
    #Splits comma-separated string into a list, and converts the list of numerical strings to int
    reference_indices = index_choice.split(",")
    for i in range(0, len(reference_indices)):
        reference_indices[i] = int(reference_indices[i])
    #With the indices, fill up a list of reference tracks by looping through each matching index of recent songs 
    reference_tracks = [recent_tracks[x-1] for x in reference_indices]
    #Uses the __str__ method in Track to print out the tracks for user
    for ref_track in reference_tracks:
        print(ref_track)
    #Ask user how many tracks to recommend
    num_tracks_to_rec = int (input("You choose the following tracks above. Now, how many "
    "tracks would you like to be recommended? Choose up to 50: "))
    #Now, we use the list of reference tracks to get a list of recommended tracks
    recommended_tracks = spotify_client.get_recs(reference_tracks, num_tracks_to_rec)
    #Uses the __str__ method in Track to print out the tracks for user
    print("Your new playlist will include these tracks:")
    for rec_track in recommended_tracks:
        print(rec_track)
    #Asks for playlist name and creates empty playlist
    playlist_name = input("What would you like to name your playlist: ")
    print(playlist_name)
    playlist = spotify_client.create_playlist(playlist_name)
    #Fills playlist with the recommended tracks
    response = spotify_client.fill_playlist(playlist, recommended_tracks)
    print(playlist.name + " was created successfully. Go check it out!")

if __name__ == "__main__":
    main()