from flask import Blueprint, jsonify, request
from app.models.invoicing import Invoicing
from app import db
import logging

logging.basicConfig(level=logging.DEBUG)

invoices_blueprint = Blueprint('invoices', __name__)

# Route to list all invoices
@invoices_blueprint.route('/', methods=['GET'])
def get_invoices():
    """Fetch all invoices."""
    try:
        invoices = Invoicing.query.all()
        result = [
            {
                "InvoiceID": invoice.InvoiceID,
                "ECControlNumber": invoice.ECControlNumber,
                "GrossAmount": float(invoice.GrossAmount or 0),
                "MemberName": invoice.MemberName
            } for invoice in invoices
        ]
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error fetching invoices: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to search an invoice by ECControlNumber
@invoices_blueprint.route('/<string:ec_control_number>', methods=['GET'])
def get_invoice_by_ec_control_number(ec_control_number):
    """Fetch a single invoice by its ECControlNumber."""
    logging.debug(f"Searching for invoice with ECControlNumber: {ec_control_number}")
    try:
        invoice = Invoicing.query.filter_by(ECControlNumber=ec_control_number).first_or_404()
        result = {
            "InvoiceID": invoice.InvoiceID,
            "BankID": invoice.BankID,
            "DestinationAssociation": invoice.DestinationAssociation,
            "ACHSettlementNumber": invoice.ACHSettlementNumber,
            "ECControlNumber": invoice.ECControlNumber,
            "MemberName": invoice.MemberName,
            "MemberID": invoice.MemberID,
            "BillingYear": invoice.BillingYear,
            "GrossAmount": float(invoice.GrossAmount or 0),
            "AssociationPortion": float(invoice.AssociationPortion or 0),
            "TransactionFee": float(invoice.TransactionFee or 0),
            "NetAssociationPortion": float(invoice.NetAssociationPortion or 0),
        }
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error fetching invoice with ECControlNumber {ec_control_number}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
