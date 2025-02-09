from flask import Blueprint, jsonify, request
from ticket_generator import generate_ticket

api_ticket_bp = Blueprint('api_ticket', __name__)

@api_ticket_bp.route('/api/ticket', methods=['POST'])
def api_ticket():
    data = request.get_json()
    generate_ticket(data)
    return jsonify({"status": "success", "message": "Ticket received"})

@api_ticket_bp.route('/api/ticket/preview', methods=['POST'])
def preview_ticket():
    data = request.get_json()
    text = data.get('text')
    # Return the ticket text for preview
    return jsonify({"status": "success", "message": "Ticket preview", "ticket": text})
