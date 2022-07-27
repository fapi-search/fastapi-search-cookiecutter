# {{ cookiecutter.project_name }}
## Docker setup
The project's docker setup is in the `./docker` directory, and includes
- A multi-stage docker build; the `development` and `production`
  stages are what you'll generally use.
- A `docker-compose.yml` for a complete working cluster, including
  Postgresql and {{ cookiecutter.search_backend | title }} services.
- A `docker-compose.env` for env vars shared across the compose
  cluster.

### Build Search Project images
Run
```bash
./scripts/build.sh
```
to produce the following images (`docker image ls`)
```
{{ cookiecutter.project_slug }}-production
{{ cookiecutter.project_slug }}-development
{{ cookiecutter.project_slug }}-builder-base
{{ cookiecutter.project_slug }}-python-base
```

Alternately, refer to the `docker build` commands in `build.sh` and build/tag as needed.

Note: we build stage-specific images for clarity, reuse and caching, and debugging.

### <a name="docker-compose"></a>Run Under docker compose
Run just the supporting `app_database` (Postgresql) and `search_database` ({{ cookiecutter.search_backend | title }}) services
```bash
docker compose -f docker/docker-compose.yml up --build
```
Add `--detach` to run in the background.

The `{{ cookiecutter.project_slug|replace('-', '_') }}_development` container mounts the project
directory and the default `CMD` runs from that, with `--reload` turned
on. You can use this to save changes on your host system and the
container will live reload. Start the development container by the
service of the same name with
```bash
docker compose -f docker/docker-compose.yml up {{ cookiecutter.project_slug|replace('-', '_') }}_development
```

If this is the first run against this database or there are new
migrations, migrate the schema with
```bash
docker compose -f docker/docker-compose.yml run --rm {{ cookiecutter.project_slug|replace('-', '_') }}_development alembic upgrade head
```

Similarly, run tests in the cluster with
```bash
docker compose -f docker/docker-compose.yml run --rm {{ cookiecutter.project_slug|replace('-', '_') }}_development ./scripts/test.sh
```
which will also recreate and migrate a clean test database. Because
the host local project folder is mounted in the container, the will
create or update `htmlcov/index.html` with a test coverage report.

Shell into the development container with
```bash
docker compose -f docker/docker-compose.yml run --rm {{ cookiecutter.project_slug|replace('-', '_') }}_development bash
```

Finally, you can run the app from its production stage container with
```bash
docker compose -f docker/docker-compose.yml up --build {{ cookiecutter.project_slug|replace('-', '_') }}_production
```
This container will, of course, not hot reload code.

## Run on your local host

### Prerequisites
- [Pyenv](https://github.com/pyenv/pyenv)
- Python >= 3.10 in `pyenv versions` list
- [Poetry](https://python-poetry.org/)

### Python env and package installation
```bash
poetry install
```
Note: You may see 0 install; the cookiecutter post processing will have done this for you.

### Postgres user and database setup
You need accessible Postgresql and {{ cookiecutter.search_backend | title }} services. (See [Run
under docker compose](#docker-compose) for a docker based solution.)

The provided `docker-compose.yml` will create a default database and
user. If not using that setup, create manually with `psql` or
equivalent:

```sql
CREATE USER db_user WITH PASSWORD 'db_pass' CREATEDB;
CREATE DATABASE app_db OWNER db_user;
```

### Run migrations
Check your database url setup in `.env`. A `sample.env` is provided to
copy in to start with. If `APP_DATABASE_URL` is not set in the
environment, a fallback setting is used from
`app/core/config.py`.
above.

```bash
poetry run alembic upgrade head
```

### {{ cookiecutter.search_backend | title }} setup

{% if cookiecutter.search_backend == "elasticsearch" -%}
Install
[Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/master/_installation.html)
and set the `SEARCH_DATABASE_URL` in your `.env` file. A `sample.env`
is provided to copy from.

Note that Elasticsearch V7, which is easier to configure, is used for
validating this repo.
{% elif cookiecutter.search_backend == "opensearch" -%}

{% endif -%}

### Run the webapp
```bash
poetry run ./scripts/run.sh
```

### Run the pre-commit linters, formatters, ...
```bash
poetry run ./scripts/lint.sh
```

### Run tests and generate code coverage files
```bash
poetry run ./scripts/test.sh
```
