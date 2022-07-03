# Search Project
## Local setup
### Prerequisites
- [Poetry](https://python-poetry.org/)
- [Pyenv](https://github.com/pyenv/pyenv)
- Python >= 3.10 in `pyenv versions` list

### Python env installation
Note: This step is a sanity check; the cookiecutter should have already run.
```bash
poetry install
```

### Postgres user and database setup
Substitute credentials and database name below with your local defaults.

In `psql` or equivalent:
```sql
CREATE USER db_user WITH PASSWORD 'db_pass' CREATEDB;
CREATE DATABASE app_db OWNER db_user;
```

Optionally, you may want `ENCODING`, `LC_COLLATE`, `LC_CTYPE`, and/or,
`TEMPLATE` settings on the `CREATE DATABASE` line. See the Postgres
[CREATE DATABASE docs](https://www.postgresql.org/docs/current/sql-createdatabase.html)
for more information. In most cases, the defaults suffice.

### Run migrations
Check your database url setup, typically in `.env`, but if
`APP_DATABASE_URL` is not set in the environment, a fallback setting
is used from `app/core/config.py`. This value should work with the
database created above.

```bash
poetry run alembic upgrade head
```

### Run the webapp
```bash
poetry run ./run.sh
```
