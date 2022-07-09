from __future__ import annotations

from databases import DatabaseURL
from opensearchpy._async.client import AsyncOpenSearch


class SearchDatabase:

    _url: DatabaseURL
    _database: AsyncOpenSearch

    def config(self, url: str | DatabaseURL) -> None:
        if hasattr(self, "_database"):
            return
        self._url = DatabaseURL(url) if isinstance(url, str) else url
        verify_certs = self._url.options.get("sslmode", "require") in [
            "require",
            "verify-ca",
            "verify-full",
        ]
        self._database = AsyncOpenSearch([str(self._url)], verify_certs=verify_certs)

    async def get_database(self) -> AsyncOpenSearch:
        assert hasattr(
            self, "_database"
        ), "Search database url not set, initialize with search_database.setup()"
        return self._database


search_database = SearchDatabase()
