from flask import Blueprint, jsonify, request
from app.models.ecp_view import DuesPaymentsSummary
from app import db

import logging
logging.basicConfig(level=logging.DEBUG)

# Define blueprint
dues_summary_blueprint = Blueprint('dues_summary', __name__)

@dues_summary_blueprint.route('/', methods=['GET'])
def get_dues_summary():
    logging.debug("Attempting to fetch dues summary...")

    """Fetch all dues payments summary."""
    try:
        # Fetch all rows from the view
        summaries = db.session.query(
            DuesPaymentsSummary.billing_association_id.label("BILLING_ASSOCIATION_ID"),
            DuesPaymentsSummary.association_name.label("ASSOCIATION_NAME"),
            DuesPaymentsSummary.null_ec_control_number.label("null_ec_control_number"),
            DuesPaymentsSummary.total_payments.label("total_payments"),
            DuesPaymentsSummary.ec_percentage.label("ec_percentage"),
        ).all()

        # Log fetched summaries for debugging
        logging.debug(f"Fetched {len(summaries)} rows from dues_payments_summary view.")

        # Transform the data for JSON response
        result = [
            {
                "BillingAssociationID": row.BILLING_ASSOCIATION_ID,
                "AssociationName": row.ASSOCIATION_NAME,
                "NullECControlNumber": row.null_ec_control_number,
                "TotalPayments": row.total_payments,
                "ECPercentage": f"{row.ec_percentage:.2f}" if row.ec_percentage is not None else "0.00",
            }
            for row in summaries
        ]

        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error fetching dues summary: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
