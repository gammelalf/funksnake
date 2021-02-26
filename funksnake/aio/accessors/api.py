import os
from datetime import datetime

from funksnake.base import Visibility
from .base import *


# ==================== #
# Library and metadata #
# ==================== #
class ArtistAccessor(ListAccessor, GetAccessor, ListLibrariesAccessor):

    url = "/api/v1/artists"


class AlbumsAccessor(ListAccessor, GetAccessor, ListLibrariesAccessor):

    url = "/api/v1/albums"


class TracksAccessor(ListAccessor, GetAccessor, ListLibrariesAccessor):

    url = "/api/v1/tracks"


# ========================= #
# Uploads and audio content #
# ========================= #
class LibraryAccessor(ListAccessor, GetAccessor, NewAccessor, UpdateAccessor, DeleteAccessor):

    url = "/api/v1/libraries/"

    async def new(self, name: str, visibility: Visibility = Visibility.ME, description: str = None):
        if description:
            description = {"description": description}
        else:
            description = {}

        return await super().new(
            data={
                "name": name,
                "visibility": visibility.value,
                **description
            }
        )


class UploadsAccessor(ListAccessor, GetAccessor, NewAccessor, UpdateAccessor, DeleteAccessor):

    url = "/api/v1/uploads/"

    async def new(self, path, library, ref=None):
        return await super().new(
            data={
                "library": library,
                "import_reference": ref or f"funksnake-import-{datetime.now().isoformat()}",
                "source": f"upload://{os.path.basename(path)}",
                "audio_file": open(path, "rb"),
            },
            timeout=0
        )

    async def metadata(self, identifier):
        return await self.session.request(
            "get", self._endpoint(identifier, "audio-file-metadata")
        )


# ================ #
# Content curation #
# ================ #
class FavoritesAccessor(ListAccessor):

    url = "/api/v1/favorites/tracks/"

    def add(self, track):
        return await self.session.request(
            "post", self._endpoint(),
            data={
                "track": track
            }
        )

    def remove(self, track):
        return await self.session.request(
            "post", self._endpoint("remove"),
            data={
                "track": track
            }
        )


class PlaylistAccessor(ListAccessor, GetAccessor, NewAccessor, UpdateAccessor, DeleteAccessor):

    url = "/api/v1/playlists/"

    async def new(self, name: str, visibility: Visibility = Visibility.ME, **kwargs):
        return await super().new(
            data={
                "name": name,
                "privacy_level": visibility.value
            }
        )

    async def add_tracks(self, identifier: str, tracks: list, allow_duplicates: bool = False):
        return await self.session.request(
            "post", self._endpoint(identifier, "add"),
            data={
                "tracks": tracks,
                "allow_duplicates": allow_duplicates
            }
        )

    async def get_tracks(self, identifier: str):
        return await self.session.request(
            "get", self._endpoint(identifier, "tracks")
        )

    async def move_tracks(self, identifier: str):
        return await self.session.request(
            "post", self._endpoint(identifier, "move")
        )

    async def remove_tracks(self, identifier):
        return await self.session.request(
            "post", self._endpoint(identifier, "remove")
        )

    async def clear_tracks(self, identifier):
        return await self.session.request(
            "delete", self._endpoint(identifier, "clear")
        )
