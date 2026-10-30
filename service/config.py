"""Configuration for the Accounts service."""
import os

# Default matches the PostgreSQL service used in CI and Kubernetes; override with DATABASE_URI.
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
