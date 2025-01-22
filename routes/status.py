from flask import Blueprint, jsonify

status_bp = Blueprint('status', __name__)

@status_bp.route('/')
def status():
    return jsonify({"status": "active", "port": 8000})
