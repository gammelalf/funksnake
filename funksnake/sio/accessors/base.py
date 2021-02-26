import os

from ..base import Session


class ApiAccessor:

    session: Session
    url: str

    def __get__(self, instance, owner):
        if instance:
            self.session = instance.session
        return self

    def _endpoint(self, *args):
        return os.path.join(self.url, *map(str, args))


class ListAccessor(ApiAccessor):

    def list(self, **kwargs):
        return self.session.request(
            "get", self._endpoint(),
            **kwargs
        )


class GetAccessor(ApiAccessor):

    def get(self, identifier, **kwargs):
        return self.session.request(
            "get", self._endpoint(identifier),
            **kwargs
        )


class ListLibrariesAccessor(ApiAccessor):

    def list_libraries(self, identifier, **kwargs):
        return self.session.request(
            "get", self._endpoint(identifier, "libraries"),
            **kwargs
        )


class NewAccessor(ApiAccessor):

    def new(self, **kwargs):
        return self.session.request(
            "post", self._endpoint(),
            **kwargs
        )


class UpdateAccessor(ApiAccessor):

    def update(self, identifier, **kwargs):
        return self.session.request(
            "post", self._endpoint(identifier),
            **kwargs
        )


class DeleteAccessor(ApiAccessor):

    def delete(self, identifier, **kwargs):
        return self.session.request(
            "delete", self._endpoint(identifier),
            **kwargs
        )
