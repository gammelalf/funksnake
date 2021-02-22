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

    async def login(self, username, password):
        async with self.session:
            await self.session.login(username, password)
