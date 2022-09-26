# Simple Mini Wallet API

## Functional Requirement

This system is used for covering cases related to money management in your wallet.

Before begin, you need to have these tools installed

* [Docker](https://www.docker.com/)
* [Postgres Docker image](https://hub.docker.com/_/postgres)
* [Liquibase Docker image](https://hub.docker.com/r/liquibase/liquibase)
* [Python](https://www.python.org/) (recommended to use [pyenv](https://github.com/pyenv/pyenv))
* [Pipenv](https://github.com/pypa/pipenv)

#### Postgres

* User `postgres`
* Password `postgrespassword`
* Port `5432`
* Container name `postgres`

## Migrations

This project is using Liquibase, read more about it [here](https://www.liquibase.org/). To run the liquibase and see all
the options, run this command:

```bash
./scripts/liquibase.sh --help
```

## Preparation

1. Start container postgres

```bash
docker container start postgres
```

2. Access container postgres

```bash
docker exec -it postgres bash
```

3. Log in into postgres instance

```bash
psql -U postgres
```

4. Create database

```sql
CREATE DATABASE mini_wallet;
```

5. Connect into database

```bash
\c mini_wallet
```

6. Create schema

```sql
CREATE DATABASE mini_wallet;
```

7. Go to your project directory and run migration

```bash
./scripts/liquibase.sh -e local
```

## Run program (console)

1. Open terminal into your project directory and install library using pipenv command

```bash
pipenv install
```

2. Activate virtual environment

```bash
pipenv shell
```

3. Run script to begin

```bash
export APP_ENV=local
export FLASK_ENV=local
export FLASK_APP=mini_wallet/app/api/app.py
python3 -m flask run
```

nb: For IDE, you can adjust it based on environment variable declared in step 3 and run it with your own way.

## Developer Test

This project is using classical approach. We are using:

1. [pytest](https://docs.pytest.org/)
2. [pytest-bdd](https://pytest-bdd.readthedocs.io/en/latest/)
3. [Postgres Docker image](https://hub.docker.com/_/postgres)

Execute the step below to run our classical test:

1. Create database `mini_wallet_unittest` and schema `mini_wallet` on your local postgres container.

2. Go to your project directory and run migration.
```bash
./scripts/liquibase.sh -e unittest
```

3. Run the tests.

```
pytest tests
```

nb: You'll also need to do this everytime there's new migration. Don't do anything to the database including insert,
update, and delete data.

## Development Tools
### MyPy

Install development dependencies and use mypy to check type annotations with command below:

```bash
dmypy run -- --namespace-packages --ignore-missing-imports .
```

or simply:

```bash
mypy .
```
