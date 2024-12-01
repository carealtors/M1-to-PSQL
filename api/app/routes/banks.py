from flask import Blueprint, jsonify, request
from app.models.bank_metadata import BankMetadata
from app import db


import logging
logging.basicConfig(level=logging.DEBUG)


# Define blueprint
banks_blueprint = Blueprint('banks', __name__)

@banks_blueprint.route('/', methods=['GET'])
def get_banks():
    logging.debug("Attempting to fetch banks...")

    """Fetch all banks."""
    try:
        banks = BankMetadata.query.all()
        result = [{"BankID": bank.BankID, "BankName": bank.BankName} for bank in banks]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
