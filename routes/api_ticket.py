from flask import Blueprint, jsonify, request
from routes.print import generate_ticket

api_ticket_bp = Blueprint('api_ticket', __name__)

@api_ticket_bp.route('/api/ticket', methods=['POST'])
def api_ticket():
    data = request.get_json()
    text = data.get('text')
    idVendor = data.get('idVendor')
    idProduct = data.get('idProduct')
    if not text or not idVendor or not idProduct:
        return jsonify({"status": "error", "message": "Missing required parameters"}), 400
    generate_ticket(text, idVendor, idProduct)
    return jsonify({"status": "success", "message": "Ticket received"})

@api_ticket_bp.route('/api/ticket/preview', methods=['POST'])
def preview_ticket():
    data = request.get_json()
    text = data.get('text')
    # Return the ticket text for preview
    return jsonify({"status": "success", "message": "Ticket preview", "ticket": text})
