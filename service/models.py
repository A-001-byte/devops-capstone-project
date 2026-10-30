"""Account model for the Accounts service."""
from datetime import date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataValidationError(Exception):
    """Raised when account data cannot be validated or deserialized."""


class Account(db.Model):
    """A customer account."""

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(32))
    date_joined = db.Column(db.Date, nullable=False, default=date.today)

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def create(self):
        """Save the account to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update the account in the database."""
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Remove the account from the database."""
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Return the account as a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat(),
        }

    def deserialize(self, data):
        """Set the account fields from a dictionary."""
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data["address"]
            self.phone_number = data.get("phone_number")
            joined = data.get("date_joined")
            if joined:
                self.date_joined = date.fromisoformat(joined)
        except KeyError as error:
            raise DataValidationError(f"Missing field: {error.args[0]}") from error
        except (TypeError, ValueError, AttributeError) as error:
            raise DataValidationError(f"Bad account data: {error}") from error
        return self

    @classmethod
    def all(cls):
        """Return every account."""
        return cls.query.all()

    @classmethod
    def find(cls, account_id):
        """Return the account with this id, or None."""
        return db.session.get(cls, account_id)

    @classmethod
    def find_by_name(cls, name):
        """Return every account with this name."""
        return cls.query.filter(cls.name == name).all()

    @staticmethod
    def init_db(app):
        """Bind the database to the app and create the tables."""
        db.init_app(app)
        with app.app_context():
            db.create_all()
