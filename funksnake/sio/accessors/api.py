from datetime import datetime

from ..base import Visibility
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

    def new(self, name: str, visibility: Visibility = Visibility.ME, description: str = None):
        if description:
            description = {"description": description}
        else:
            description = {}

        return super().new(
            data={
                "name": name,
                "visibility": visibility.value,
                **description
            }
        )


class UploadsAccessor(ListAccessor, GetAccessor, NewAccessor, UpdateAccessor, DeleteAccessor):

    url = "/api/v1/uploads/"

    def new(self, path, library, ref=None):
        return super().new(
            data={
                "library": library,
                "import_reference": ref or f"funksnake-import-{datetime.now().isoformat()}",
                "source": f"upload://{os.path.basename(path)}",
                "audio_file": open(path, "rb"),
            },
            timeout=0
        )

    def metadata(self, identifier):
        return self.session.request(
            "get", self._endpoint(identifier, "audio-file-metadata")
        )


# ================ #
# Content curation #
# ================ #
class FavoritesAccessor(ListAccessor):

    url = "/api/v1/favorites/tracks/"

    def add(self, track):
        return self.session.request(
            "post", self._endpoint(),
            data={
                "track": track
            }
        )

    def remove(self, track):
        return self.session.request(
            "post", self._endpoint("remove"),
            data={
                "track": track
            }
        )


class PlaylistAccessor(ListAccessor, GetAccessor, NewAccessor, UpdateAccessor, DeleteAccessor):

    url = "/api/v1/playlists/"

    def new(self, name: str, visibility: Visibility = Visibility.ME, **kwargs):
        return super().new(
            data={
                "name": name,
                "privacy_level": visibility.value
            }
        )

    def add_tracks(self, identifier: str, tracks: list, allow_duplicates: bool = False):
        return self.session.request(
            "post", self._endpoint(identifier, "add"),
            data={
                "tracks": tracks,
                "allow_duplicates": allow_duplicates
            }
        )

    def get_tracks(self, identifier: str):
        return self.session.request(
            "get", self._endpoint(identifier, "tracks")
        )

    def move_tracks(self, identifier: str):
        return self.session.request(
            "post", self._endpoint(identifier, "move")
        )

    def remove_tracks(self, identifier):
        return self.session.request(
            "post", self._endpoint(identifier, "remove")
        )

    def clear_tracks(self, identifier):
        return self.session.request(
            "delete", self._endpoint(identifier, "clear")
        )
