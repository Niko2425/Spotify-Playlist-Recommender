# Spotify-Playlist-Recommender
A Python script that uses Spotify's API to recommend a user a playlist of songs based on recently played tracks in a user's profile. 

Requires requests and json modules, and before running the program, the user must set their unique Spotify API Authorization Token and User ID like so:

`set AUTH_TOKEN=paste_auth_token_here`

`set USER_ID=paste_user_id_here`

The Authorization Token can be found [here](https://developer.spotify.com/console/post-playlists/), making sure to check the scopes for playlist-modify-public, playlist-modify-private, and user-read-recently-played.

The User ID can be found here [here](https://developer.spotify.com/console/get-current-user/).

After the user sets the values, simply run the script like so:

`python recommendplaylist.py`

