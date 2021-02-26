import os
from enum import Enum

import aiohttp


class Visibility(Enum):
    ME = "me"
    INSTANCE = "instance"
    EVERYONE = "everyone"


class Session:
    """
    This class handles the actual http requests and the authentication
    """

    token: str
    session: aiohttp.ClientSession

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None
        self.token = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            # timeout=aiohttp.ClientTimeout(total=10),
            headers={"User-Agent": "funkwhale/cli"}
        )
        await self.session.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)
            self.session = None

    async def login(self, username, password):
        response = await self.session.post(
            f"{self.base_url}/api/v1/token",
            data={"username": username, "password": password}
        )
        if response.status == 400:
            raise RuntimeError("Unable to log in")
        else:
            self.token = (await response.json())["token"]

    async def request(self, method: str, url: str, *args, **kwargs):
        if url.startswith("http://") or url.startswith("https://"):
            full_url = url
        else:
            full_url = self.base_url + url
        headers = kwargs.setdefault("headers", {})
        if self.token:
            scheme = "JWT" if len(self.token) > 50 else "Bearer"
            headers["Authorization"] = f"{scheme} {self.token}"
        response = await getattr(self.session, method)(full_url, *args, **kwargs)
        response.raise_for_status()
        return await response.json()
