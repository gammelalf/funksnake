from json import JSONDecodeError

import requests

from .accessors.api import *


class Funkwhale:
    """
    This class handles the actual http requests and the authentication
    """

    token: str

    artists = ArtistAccessor()
    albums = AlbumsAccessor()
    tracks = TracksAccessor()
    libraries = LibraryAccessor()
    uploads = UploadsAccessor()
    favourites = FavoritesAccessor()
    playlists = PlaylistAccessor()

    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

    def login(self, username, password):
        response = self.request(
            "post", "/api/v1/token",
            data={"username": username, "password": password}
        )
        self.token = response["token"]

    def request(self, method: str, url: str, *args, **kwargs):
        if url.startswith("http://") or url.startswith("https://"):
            full_url = url
        else:
            full_url = self.base_url + url

        headers = kwargs.setdefault("headers", {})
        headers.setdefault("User-Agent", "funkwhale-api")
        if self.token:
            scheme = "JWT" if len(self.token) > 50 else "Bearer"
            headers.setdefault("Authorization", f"{scheme} {self.token}")

        response = getattr(requests, method)(full_url, *args, **kwargs)
        response.raise_for_status()
        try:
            return response.json()
        # /libraries/fs_import returns an empty string
        except JSONDecodeError:
            return response.text
