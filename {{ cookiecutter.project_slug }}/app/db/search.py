from __future__ import annotations

from databases import DatabaseURL

# use from app.db.search import AsyncSearch for portability
{% if cookiecutter.search_backend == "elasticsearch" -%}
from elasticsearch import AsyncElasticsearch as AsyncSearch
{% elif cookiecutter.search_backend == "opensearch" -%}
from opensearchpy._async.client import AsyncOpenSearch as AsyncSearch
{% endif %}

class SearchDatabase:

    _url: DatabaseURL
    _database: AsyncSearch

    def config(self, url: str | DatabaseURL) -> None:
        if hasattr(self, "_database"):
            return
        self._url = DatabaseURL(url) if isinstance(url, str) else url
        self.verify_certs = self._url.options.get("sslmode", "require") in [
            "require",
            "verify-ca",
            "verify-full",
        ]

    async def connect(self) -> None:
        assert hasattr(
            self, "_url"
        ), "Search database url not set, initialize with search_database.setup()"
        self._database = AsyncSearch([str(self._url)], verify_certs=self.verify_certs)

    async def disconnect(self) -> None:
        assert hasattr(
            self, "_url"
        ), "Search database url not set, initialize with search_database.setup()"
        await self._database.close()

    async def get_database(self) -> AsyncSearch:
        assert hasattr(
            self, "_url"
        ), "Search database url not set, initialize with search_database.setup()"
        return self._database


search_database = SearchDatabase()
