# Search Project
## Local setup
### Prerequisites
- [Pyenv](https://github.com/pyenv/pyenv)
- Python >= 3.10 in `pyenv versions` list
- [Poetry](https://python-poetry.org/)

### Python env installation
Note: You may see 0 install; the cookiecutter post processing will have done this for you.
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

### Get an "{{ cookiecutter.search_backend|capitalize }}" service up
See the {% if cookiecutter.search_backend == 'elasticsearch' %}[Elasticsearch install docs](https://www.elastic.co/guide/en/elasticsearch/reference/master/_installation.html){% elif cookiecutter.search_backend == 'opensearch' %}[Opensearch install docs](https://opensearch.org/docs/latest/opensearch/install/index/){% endif -%} for more information.

{% if cookiecutter.search_backend == 'elasticsearch' -%}
Note that presently this project is tested against v7, but should work with later versions.
{% endif -%}

### Double check env vars

This project will look for a top level `.env` file. A `sample.env` is provided to copy from.

### Run the webapp
```bash
poetry run ./run.sh
```

### Run the pre-commit linters, formatters, ...
```bash
poetry run pre-commit run --all-files
```

### Build and run the docker image
```bash
docker build -t {{ cookiecutter.project_slug }} -f docker/Dockerfile .
docker run -p {{ cookiecutter.default_docker_port }}:{{ cookiecutter.default_docker_port }} \
	-e 'APP_DATABASE_URL=$(APP_DATABASE_URL) -e 'SEARCH_DATABASE_URL=$(SEARCH_DATABASE_URL) \
	{{ cookiecutter.project_slug }}
```
where `APP_DATABASE_URL` and `SEARCH_DATABASE_URL` are urls accessible from the container's networking.
