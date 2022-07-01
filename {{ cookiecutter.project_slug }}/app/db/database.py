from __future__ import annotations

from databases import Database, DatabaseURL

from app.core.config import settings


class AppDatabase:

    _url: DatabaseURL
    _database: Database

    async def setup(self, url: str | DatabaseURL) -> None:
        self._url = DatabaseURL(url) if isinstance(url, str) else url
        self._database = Database(self._url)
        await self._database.connect()

    async def get_database(self) -> Database:
        if not self._database:
            raise Exception(
                "App database url not set, initialize with app_database.setup()"
            )
        return Database(settings.APP_DATABASE_URL)


app_database = AppDatabase()
