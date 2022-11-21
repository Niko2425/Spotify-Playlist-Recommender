class Track:
    #Constructor
    def __init__(self, name, id, artist):
        """
        :param name (str): Track name
        :param id (int): Track ID
        :param artist (str): Artist name
        """
        #essentially this.x in Java
        self.name = name
        self.id = id
        self.artist = artist

    #Creates a URI link that'll be used to add tracks into playlists
    def create_uri(self):
        return "spotify:track:" + self.id 
    
    #String method of object that will let us print the track's name and artists with ease
    def __str__(self):
        return self.name + " by " + self.artist

class Playlist:
    #Constructor
    def __init__(self, name, id):
        """
        :param name (str): Playlist name
        :param id (int): Playlist ID
        """
        self.name = name
        self.id = id