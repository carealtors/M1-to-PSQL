from flask import Blueprint, jsonify, request
from app.models.manual_eft import ManualEFT
from app import db

efts_blueprint = Blueprint('efts', __name__)

@efts_blueprint.route('/', methods=['GET'])
def get_efts():
    try:
        efts = ManualEFT.query.all()
        result = [{"EFTID": eft.EFTID, "Amount": float(eft.Amount or 0)} for eft in efts]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
