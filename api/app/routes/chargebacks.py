from flask import Blueprint, jsonify, request
from app.models.chargeback import Chargeback
from app import db

chargebacks_blueprint = Blueprint('chargebacks', __name__)

@chargebacks_blueprint.route('/', methods=['GET'])
def get_chargebacks():
    try:
        chargebacks = Chargeback.query.all()
        result = [{"ChargebackID": chargeback.ChargebackID, "Amount": float(chargeback.Amount or 0)} for chargeback in chargebacks]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
