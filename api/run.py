from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import psycopg2

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Define the BankMetadata model
class BankMetadata(db.Model):
    __tablename__ = 'BankMetadata'

    BankID = db.Column(db.Integer, primary_key=True)
    BankName = db.Column(db.String)
    AssociationCode = db.Column(db.String)
    AssociationName = db.Column(db.String)


# Define the Invoicing model
class Invoicing(db.Model):
    __tablename__ = 'Invoicing'

    InvoiceID = db.Column(db.Integer, primary_key=True)
    BankID = db.Column(db.Integer, db.ForeignKey('BankMetadata.BankID'))
    DestinationAssociation = db.Column(db.String)
    ACHSettlementNumber = db.Column(db.String)
    ECControlNumber = db.Column(db.String)
    MemberName = db.Column(db.String)
    MemberID = db.Column(db.BigInteger)
    BillingYear = db.Column(db.Integer)
    GrossAmount = db.Column(db.Numeric)
    AssociationPortion = db.Column(db.Numeric)
    TransactionFee = db.Column(db.Numeric)
    NetAssociationPortion = db.Column(db.Numeric)


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    """Health check endpoint to verify database connectivity."""
    try:
        connection = psycopg2.connect(DATABASE_URL)
        connection.close()
        return jsonify({"status": "success", "message": "Database is reachable"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/banks', methods=['GET'])
def get_banks():
    """Fetch all records from the BankMetadata table."""
    try:
        banks = BankMetadata.query.all()
        result = []
        for bank in banks:
            result.append({
                "BankID": bank.BankID,
                "BankName": bank.BankName,
                "AssociationCode": bank.AssociationCode,
                "AssociationName": bank.AssociationName
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/invoices/<string:ec_control_number>', methods=['GET'])
def get_invoices_by_ec_control_number(ec_control_number):
    """Fetch invoices filtered by EC Control Number."""
    try:
        invoices = Invoicing.query.filter_by(ECControlNumber=ec_control_number).all()
        if not invoices:
            return jsonify({"status": "error", "message": "No invoices found for the specified EC Control Number"}), 404

        result = []
        for invoice in invoices:
            result.append({
                "InvoiceID": invoice.InvoiceID,
                "BankID": invoice.BankID,
                "DestinationAssociation": invoice.DestinationAssociation,
                "ACHSettlementNumber": invoice.ACHSettlementNumber,
                "ECControlNumber": invoice.ECControlNumber,
                "MemberName": invoice.MemberName,
                "MemberID": invoice.MemberID,
                "BillingYear": invoice.BillingYear,
                "GrossAmount": str(invoice.GrossAmount),
                "AssociationPortion": str(invoice.AssociationPortion),
                "TransactionFee": str(invoice.TransactionFee),
                "NetAssociationPortion": str(invoice.NetAssociationPortion),
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("FLASK_PORT", 5000)))
