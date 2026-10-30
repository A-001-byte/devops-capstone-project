"""Test Cases for Account Model."""
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
    """Test Cases for Account Model."""

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

    def test_create_an_account(self):
        """It should Create an account and add it to the database"""
        self.assertEqual(Account.all(), [])
        account = Account().deserialize(SAMPLE)
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_add_an_account(self):
        """It should Create an Account and assert that it exists"""
        account = Account().deserialize(SAMPLE)
        self.assertIsNotNone(account)
        self.assertEqual(account.id, None)
        self.assertEqual(account.name, "Ada Lovelace")
        self.assertEqual(account.date_joined, date(2024, 1, 15))

    def test_delete_an_account(self):
        """It should Delete an account from the database"""
        account = Account().deserialize(SAMPLE)
        account.create()
        self.assertEqual(len(Account.all()), 1)
        account.delete()
        self.assertEqual(Account.all(), [])
        self.assertIsNone(Account.find(account.id))

    def test_deserialize_an_account(self):
        """It should Deserialize an account"""
        account = Account().deserialize(SAMPLE)
        self.assertEqual(account.email, "ada@example.com")
        self.assertEqual(account.address, "12 Analytical St")
        self.assertEqual(account.phone_number, "555-0100")

    def test_deserialize_with_key_error(self):
        """It should not Deserialize an account with a KeyError"""
        with self.assertRaises(DataValidationError):
            Account().deserialize({"name": "No Email"})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize an account with a TypeError"""
        with self.assertRaises(DataValidationError):
            Account().deserialize("not a dict")
        with self.assertRaises(DataValidationError):
            Account().deserialize({**SAMPLE, "date_joined": "yesterday"})

    def test_find_by_name(self):
        """It should Find an Account by name"""
        Account().deserialize(SAMPLE).create()
        found = Account.find_by_name("Ada Lovelace")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].email, "ada@example.com")
        self.assertEqual(Account.find_by_name("Nobody"), [])

    def test_list_all_accounts(self):
        """It should List all Accounts in the database"""
        Account().deserialize(SAMPLE).create()
        Account().deserialize({**SAMPLE, "name": "Alan Turing"}).create()
        self.assertEqual(len(Account.all()), 2)

    def test_read_an_account(self):
        """It should Read an account"""
        account = Account().deserialize(SAMPLE)
        account.create()
        found = Account.find(account.id)
        self.assertEqual(found.id, account.id)
        self.assertEqual(found.name, "Ada Lovelace")
        self.assertIn("Ada Lovelace", repr(found))

    def test_serialize_an_account(self):
        """It should Serialize an account"""
        account = Account().deserialize(SAMPLE)
        account.create()
        data = account.serialize()
        self.assertEqual(data["id"], account.id)
        self.assertEqual(data["name"], "Ada Lovelace")
        self.assertEqual(data["date_joined"], "2024-01-15")

    def test_update_an_account(self):
        """It should Update an account"""
        account = Account().deserialize(SAMPLE)
        account.create()
        account.name = "Augusta Ada King"
        account.update()
        self.assertEqual(Account.find(account.id).name, "Augusta Ada King")
        with self.assertRaises(DataValidationError):
            Account().deserialize(SAMPLE).update()
