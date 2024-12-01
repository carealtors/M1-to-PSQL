from flask import Flask, jsonify
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

    MetadataID = db.Column(db.Integer, primary_key=True)
    AssociationCode = db.Column(db.String)
    AssociationName = db.Column(db.String)
    BankID = db.Column(db.Integer)
    BankName = db.Column(db.String)


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    """Health check endpoint to verify database connectivity."""
    try:
        # Test database connection
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
                "MetadataID": bank.MetadataID,
                "AssociationCode": bank.AssociationCode,
                "AssociationName": bank.AssociationName,
                "BankID": bank.BankID,
                "BankName": bank.BankName
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("FLASK_PORT", 5000)))