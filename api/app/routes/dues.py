from flask import Blueprint, jsonify, request
from app.models.dues import DuesPayments  # Import the DuesPayments model
from app import db
import logging

logging.basicConfig(level=logging.DEBUG)

dues_blueprint = Blueprint('dues', __name__)

# Route to search for dues payments by MEMBER_ID and BILLING_YEAR
@dues_blueprint.route('/<int:member_id>/<int:year>', methods=['GET'])
def get_dues_by_member_and_year(member_id, year):
    """Fetch dues details for a member by MEMBER_ID and BILLING_YEAR."""
    logging.debug(f"Searching for dues for Member ID: {member_id} and Year: {year}")
    
    try:
        # Query all rows matching MEMBER_ID and BILLING_YEAR
        dues = DuesPayments.query.filter(
            DuesPayments.MEMBER_ID == member_id,
            DuesPayments.BILLING_YEAR == year
        ).all()
        
        if not dues:
            return jsonify({"status": "error", "message": f"No dues found for Member ID: {member_id} in {year}"}), 404
        
        result = [
            {
                "MEMBER_ID": dues_entry.MEMBER_ID,
                "MEMBER_FIRST_NAME": dues_entry.MEMBER_FIRST_NAME,
                "MEMBER_LAST_NAME": dues_entry.MEMBER_LAST_NAME,
                "INCURRING_MEMBER_ID": dues_entry.INCURRING_MEMBER_ID,
                "INCURRING_MEMBER_FIRST_NAME": dues_entry.INCURRING_MEMBER_FIRST_NAME,
                "INCURRING_MEMBER_LAST_NAME": dues_entry.INCURRING_MEMBER_LAST_NAME,
                "PRIMARY_ASSOCIATION_ID": dues_entry.PRIMARY_ASSOCIATION_ID,
                "PRIMARY_STATE_ASSOCIATION_ID": dues_entry.PRIMARY_STATE_ASSOCIATION_ID,
                "BILLING_ASSOCIATION_ID": dues_entry.BILLING_ASSOCIATION_ID,
                "OFFICE_ID": dues_entry.OFFICE_ID,
                "PAYMENT_TYPE_CODE": dues_entry.PAYMENT_TYPE_CODE,
                "BILLING_YEAR": dues_entry.BILLING_YEAR,
                "PAYMENT_AMOUNT": float(dues_entry.PAYMENT_AMOUNT or 0),
                "CONTRIBUTION_TYPE_CODE": dues_entry.CONTRIBUTION_TYPE_CODE,
                "DUES_PAID_DATE": str(dues_entry.DUES_PAID_DATE),
                "PAYMENT_SOURCE_CODE": dues_entry.PAYMENT_SOURCE_CODE,
                "EC_CONTROL_NUMBER": dues_entry.EC_CONTROL_NUMBER,
                "LAST_CHANGED_BY": dues_entry.LAST_CHANGED_BY,
                "LAST_CHANGED_DATETIME": str(dues_entry.LAST_CHANGED_DATETIME)
            }
            for dues_entry in dues
        ]
        
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error fetching dues for Member ID: {member_id} in Year: {year}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


# Route to search for dues payments by MEMBER_ID, BIL
