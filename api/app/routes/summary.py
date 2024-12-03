from flask import Blueprint, jsonify
from app.models import Invoicing, ManualEFT, Chargeback
from app.utils import format_currency
from sqlalchemy.sql import func
from app import db

summary_blueprint = Blueprint('summary', __name__)

@summary_blueprint.route('/', methods=['GET'])
def get_summary():
    try:
        # Aggregate data
        total_invoicing_amount = db.session.query(func.sum(Invoicing.GrossAmount)).scalar() or 0
        invoicing_count = db.session.query(func.count(Invoicing.InvoiceID)).scalar()

        total_manual_eft_amount = db.session.query(func.sum(ManualEFT.Amount)).scalar() or 0
        manual_eft_count = db.session.query(func.count(ManualEFT.EFTID)).scalar()

        total_chargeback_amount = db.session.query(func.sum(Chargeback.Amount)).scalar() or 0
        chargeback_count = db.session.query(func.count(Chargeback.ChargebackID)).scalar()

        # Combine results
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
