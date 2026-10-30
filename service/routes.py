"""Routes for the Accounts REST API."""
from flask import abort, jsonify, request, url_for

from service import app
from service.common import status
from service.models import Account


def check_content_type(media_type):
    """Abort with 415 unless the request has the expected content type."""
    if request.headers.get("Content-Type", "") != media_type:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {media_type}")


@app.route("/health")
def health():
    """Report that the service is up."""
    return jsonify(status="OK"), status.HTTP_200_OK


@app.route("/")
def index():
    """Describe the service and where its resources live."""
    return jsonify(name="Account REST API Service", version="1.0"), status.HTTP_200_OK


@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Create an account from the JSON body."""
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    location_url = url_for("read_accounts", account_id=account.id, _external=True)
    return (
        jsonify(account.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all accounts."""
    accounts = [account.serialize() for account in Account.all()]
    return jsonify(accounts), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_accounts(account_id):
    """Read one account."""
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    return jsonify(account.serialize()), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Update one account from the JSON body."""
    check_content_type("application/json")
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    account.deserialize(request.get_json())
    account.update()
    return jsonify(account.serialize()), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Delete one account if it exists."""
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", status.HTTP_204_NO_CONTENT
