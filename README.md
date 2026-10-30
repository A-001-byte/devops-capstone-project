# Customer Accounts Microservice

![Build Status](https://github.com/A-001-byte/Devops-Capstone-Final-submission-/actions/workflows/ci-build.yaml/badge.svg)

A REST microservice that manages customer accounts. It is built with Flask and
PostgreSQL, tested with nose, checked with flake8 and pylint, secured with
Flask-Talisman and CORS, and packaged as a Docker image for Kubernetes.

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Service name, version and links |
| GET | `/health` | Health check |
| POST | `/accounts` | Create an account |
| GET | `/accounts` | List all accounts |
| GET | `/accounts/<id>` | Read one account |
| PUT | `/accounts/<id>` | Update an account |
| DELETE | `/accounts/<id>` | Delete an account |

An account has `name`, `email`, `address`, an optional `phone_number` and a
`date_joined` date (`YYYY-MM-DD`).

## Run the tests

```bash
pip install -r requirements.txt
export DATABASE_URI=postgresql://postgres:postgres@localhost:5432/postgres
nosetests
```

## Run the service

```bash
flask --app service run --port 8000
```

## Container

```bash
docker build -t accounts:1 .
docker run -p 8080:8080 -e DATABASE_URI=<your-database-uri> accounts:1
```
