"""Test cases for the Account model."""
import unittest
from datetime import date

from service import app
from service.models import Account, DataValidationError, db

SAMPLE = {
    "name": "Ada Lovelace",
    "email": "ada@example.com",
    "address": "12 Analytical St",
    "phone_number": "555-0100",
    "date_joined": "2024-01-15",
}


class TestAccountModel(unittest.TestCase):
    """Exercise create, read, update, delete and (de)serialization."""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.context = app.app_context()
        cls.context.push()

    @classmethod
    def tearDownClass(cls):
        cls.context.pop()

    def setUp(self):
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_create_and_find(self):
        """A saved account can be found again."""
        account = Account().deserialize(SAMPLE)
        account.create()
        self.assertIsNotNone(account.id)
        self.assertEqual(Account.find(account.id).name, "Ada Lovelace")
        self.assertEqual(len(Account.all()), 1)

    def test_serialize_round_trip(self):
        """Serializing then deserializing keeps the data."""
        account = Account().deserialize(SAMPLE)
        account.create()
        data = account.serialize()
        self.assertEqual(data["date_joined"], "2024-01-15")
        again = Account().deserialize(data)
        self.assertEqual(again.email, SAMPLE["email"])
        self.assertEqual(again.date_joined, date(2024, 1, 15))

    def test_update(self):
        """Updating changes the stored data."""
        account = Account().deserialize(SAMPLE)
        account.create()
        account.name = "Augusta Ada King"
        account.update()
        self.assertEqual(Account.find(account.id).name, "Augusta Ada King")

    def test_update_without_id(self):
        """Updating an unsaved account is an error."""
        with self.assertRaises(DataValidationError):
            Account().deserialize(SAMPLE).update()

    def test_delete(self):
        """A deleted account is gone."""
        account = Account().deserialize(SAMPLE)
        account.create()
        account.delete()
        self.assertEqual(Account.all(), [])
        self.assertIsNone(Account.find(account.id))

    def test_deserialize_missing_field(self):
        """Missing required fields are rejected."""
        with self.assertRaises(DataValidationError):
            Account().deserialize({"name": "No Email"})

    def test_deserialize_bad_data(self):
        """Non-dictionary data and bad dates are rejected."""
        with self.assertRaises(DataValidationError):
            Account().deserialize("not a dict")
        with self.assertRaises(DataValidationError):
            Account().deserialize({**SAMPLE, "date_joined": "yesterday"})

    def test_repr(self):
        """The repr names the account."""
        account = Account().deserialize(SAMPLE)
        self.assertIn("Ada Lovelace", repr(account))
