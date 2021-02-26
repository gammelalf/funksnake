from .accessors.api import *
from .base import Session


class Funkwhale:

    artists = ArtistAccessor()
    albums = AlbumsAccessor()
    tracks = TracksAccessor()
    libraries = LibraryAccessor()
    uploads = UploadsAccessor()
    favourites = FavoritesAccessor()
    playlists = PlaylistAccessor()

    def __init__(self, base_url):
        self.session = Session(base_url)

    def login(self, username, password):
        self.session.login(username, password)
