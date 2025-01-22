from flask import Flask, request, send_file
from ticket_generator import generate_ticket

app = Flask(__name__)

@app.route('/api/ticket', methods=['POST'])
def create_ticket():
    ticket_data = request.json
    generate_ticket(ticket_data)
    return send_file('ticket.pdf', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
