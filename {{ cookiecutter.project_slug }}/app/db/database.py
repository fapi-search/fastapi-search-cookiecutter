from __future__ import annotations

from databases import Database, DatabaseURL


class AppDatabase:

    _url: DatabaseURL
    _database: Database

    def config(self, url: str | DatabaseURL, force_rollback: bool = False) -> None:
        if hasattr(self, "_database"):
            return
        self._url = DatabaseURL(url) if isinstance(url, str) else url
        self._database = Database(self._url, force_rollback=force_rollback)

    async def connect(self) -> None:
        assert hasattr(
            self, "_database"
        ), "App database url not set, initialize with app_database.setup()"
        try:
            await self._database.connect()
        except OSError as e:
            print(f"Connect to {self._url.obscure_password} failed: {e}")

    async def disconnect(self) -> None:
        assert hasattr(
            self, "_database"
        ), "App database url not set, initialize with app_database.setup()"
        await self._database.disconnect()

    async def get_database(self) -> Database:
        assert hasattr(
            self, "_database"
        ), "App database url not set, initialize with app_database.setup()"
        return self._database


app_database = AppDatabase()
