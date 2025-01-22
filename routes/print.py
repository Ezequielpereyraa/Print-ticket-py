from flask import Blueprint, jsonify, request
from escpos import printer
from escpos.exceptions import USBNotFoundError
import usb.core
import usb.util

print_bp = Blueprint('print', __name__)

def generate_ticket(text, idVendor=None, idProduct=None):
    """
    Generate and print a ticket using a thermal printer.

    :param text: The text content of the ticket.
    :param idVendor: The vendor ID of the USB printer.
    :param idProduct: The product ID of the USB printer.
    """
    try:
        if idVendor and idProduct:
            p = printer.Usb(idVendor, idProduct)
        else:
            raise ValueError("idVendor and idProduct must be provided")
        p.text(text)
        p.cut()
    except USBNotFoundError:
        print("Printer not found. Please check the connection and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

def list_usb_printers():
    """
    List all connected USB printers.

    :return: A list of connected USB printers.
    """
    printers = []
    for device in usb.core.find(find_all=True):
        if device.bDeviceClass == 7:  # 7 is the USB class code for printers
            printers.append(usb.util.get_string(device, device.iProduct))
    if not printers:
        return ["No printers connected"]
    return printers

@print_bp.route('/print/list', methods=['GET'])
def list_devices():
    printers = list_usb_printers()
    return jsonify({"status": "active", "port": 8000, "printers": printers})

@print_bp.route('/print', methods=['POST'])
def print_ticket():
    data = request.get_json()
    text = data.get('text')
    idVendor = data.get('idVendor')
    idProduct = data.get('idProduct')
    if not text or not idVendor or not idProduct:
        return jsonify({"status": "error", "message": "Missing required parameters"}), 400
    generate_ticket(text, idVendor, idProduct)
    return jsonify({"status": "success", "message": "Ticket printed successfully"})
