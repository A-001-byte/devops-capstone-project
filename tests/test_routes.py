"""Account Service Tests."""
import unittest

from service import app, talisman
from service.common import status
from service.models import Account, db

BASE_URL = "/accounts"
HTTPS_ENVIRON = {"wsgi.url_scheme": "https"}
SAMPLE = {
    "name": "Grace Hopper",
    "email": "grace@example.com",
    "address": "1 Compiler Way",
    "phone_number": "555-0199",
    "date_joined": "2024-02-20",
}


class TestAccountService(unittest.TestCase):
    """Account Service Tests."""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.logger.setLevel("CRITICAL")
        talisman.force_https = False
        cls.context = app.app_context()
        cls.context.push()

    @classmethod
    def tearDownClass(cls):
        cls.context.pop()

    def setUp(self):
        db.session.query(Account).delete()
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()

    def _create(self, **overrides):
        response = self.client.post(BASE_URL, json={**SAMPLE, **overrides})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.get_json()

    def test_index(self):
        """It should get 200_OK from the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.get_json(), {"name": "Account REST API Service", "version": "1.0"}
        )

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["status"], "OK")

    def test_create_account(self):
        """It should Create a new Account"""
        response = self.client.post(BASE_URL, json=SAMPLE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("/accounts/", response.headers["Location"])
        self.assertEqual(response.get_json()["name"], "Grace Hopper")

    def test_create_account_bad_data(self):
        """It should not Create an Account when sending the wrong data"""
        response = self.client.post(BASE_URL, json={"name": "No Email"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_wrong_media_type(self):
        """It should not Create an Account when sending the wrong media type"""
        response = self.client.post(BASE_URL, data="x", content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_get_account_list(self):
        """It should Get a list of Accounts"""
        self._create()
        self._create(name="Alan Turing", email="alan@example.com")
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.get_json()), 2)

    def test_get_account(self):
        """It should Read a single Account"""
        created = self._create()
        response = self.client.get(f"{BASE_URL}/{created['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["email"], "grace@example.com")

    def test_get_account_not_found(self):
        """It should not Read an Account that is not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_account(self):
        """It should Update an existing Account"""
        created = self._create()
        created["name"] = "Rear Admiral Hopper"
        response = self.client.put(f"{BASE_URL}/{created['id']}", json=created)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["name"], "Rear Admiral Hopper")
        missing = self.client.put(f"{BASE_URL}/0", json=SAMPLE)
        self.assertEqual(missing.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_account(self):
        """It should Delete an Account"""
        created = self._create()
        response = self.client.delete(f"{BASE_URL}/{created['id']}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"{BASE_URL}/{created['id']}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        response = self.client.delete(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_security_headers(self):
        """It should return security headers"""
        response = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        headers = {
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'self'; object-src 'none'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        for key, value in headers.items():
            self.assertEqual(response.headers.get(key), value)

    def test_cors_security(self):
        """It should return a CORS header"""
        response = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")
