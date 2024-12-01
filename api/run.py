import locale
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Set locale for currency formatting
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Define models
class BankMetadata(db.Model):
    __tablename__ = 'BankMetadata'

    BankID = db.Column(db.Integer, primary_key=True)
    BankName = db.Column(db.String)
    AssociationCode = db.Column(db.String)
    AssociationName = db.Column(db.String)


class Invoicing(db.Model):
    __tablename__ = 'Invoicing'

    InvoiceID = db.Column(db.Integer, primary_key=True)
    BankID = db.Column(db.Integer, db.ForeignKey('BankMetadata.BankID'))
    GrossAmount = db.Column(db.Numeric)


class ManualEFT(db.Model):
    __tablename__ = 'ManualEFT'

    EFTID = db.Column(db.Integer, primary_key=True)
    BankID = db.Column(db.Integer, db.ForeignKey('BankMetadata.BankID'))
    Amount = db.Column(db.Numeric)


class Chargeback(db.Model):
    __tablename__ = 'Chargeback'

    ChargebackID = db.Column(db.Integer, primary_key=True)
    BankID = db.Column(db.Integer, db.ForeignKey('BankMetadata.BankID'))
    Amount = db.Column(db.Numeric)


def format_currency(amount):
    """Format a numeric value as a dollar currency string."""
    return locale.currency(amount, grouping=True) if amount is not None else "$0.00"


@app.route('/summary', methods=['GET'])
def get_summary():
    """Provide a summary of data across all tables."""
    try:
        # Aggregate data from Invoicing
        total_invoicing_amount = db.session.query(func.sum(Invoicing.GrossAmount)).scalar() or 0
        invoicing_count = db.session.query(func.count(Invoicing.InvoiceID)).scalar()

        # Aggregate data from Manual EFT
        total_manual_eft_amount = db.session.query(func.sum(ManualEFT.Amount)).scalar() or 0
        manual_eft_count = db.session.query(func.count(ManualEFT.EFTID)).scalar()

        # Aggregate data from Chargeback
        total_chargeback_amount = db.session.query(func.sum(Chargeback.Amount)).scalar() or 0
        chargeback_count = db.session.query(func.count(Chargeback.ChargebackID)).scalar()

        # Combine results with formatted amounts
        summary = {
            "invoicing": {
                "total_gross_amount": format_currency(total_invoicing_amount),
                "record_count": invoicing_count,
            },
            "manual_eft": {
                "total_amount": format_currency(total_manual_eft_amount),
                "record_count": manual_eft_count,
            },
            "chargeback": {
                "total_amount": format_currency(total_chargeback_amount),
                "record_count": chargeback_count,
            },
        }

        return jsonify(summary), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("FLASK_PORT", 5000)))
