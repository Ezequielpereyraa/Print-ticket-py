import os
import win32print
import win32api
from fastapi import FastAPI
from pydantic import BaseModel
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

app = FastAPI()

# Modelo de datos para la solicitud
class OrderItem(BaseModel):
    title: str
    variants: list[dict]

class OrderData(BaseModel):
    name: str
    date: str
    address: str
    addressReference: str
    ws: str
    note: str
    order: list[OrderItem]
    shipping: str
    priceDelivery: float
    appliedDiscount: float
    totalAmmount: float
    printer_name: str  # Nombre de la impresora

# Función para generar el ticket en PDF
def generate_ticket(order_data: OrderData):
    file_name = "ticket.pdf"
    width = 58 * mm
    height = 200 * mm

    c = canvas.Canvas(file_name, pagesize=(width, height))

    # Información del ticket
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 20, "Freakys Burgers")
    y_position = height - 40

    c.setFont("Helvetica", 10)
    c.drawString(10, y_position, f"Cliente: {order_data.name}")
    y_position -= 15
    c.drawString(10, y_position, f"Fecha: {order_data.date}")
    y_position -= 15
    c.drawString(10, y_position, f"Dirección: {order_data.address}")
    y_position -= 15
    c.drawString(10, y_position, f"Referencia: {order_data.addressReference}")
    y_position -= 15
    c.drawString(10, y_position, f"Teléfono: {order_data.ws}")
    y_position -= 15

    # Detalles del pedido
    c.setFont("Helvetica-Bold", 10)
    c.drawString(10, y_position, "Detalles del Pedido")
    c.setFont("Helvetica", 8)
    y_position -= 15

    for item in order_data.order:
        for variant in item.variants:
            text = f"{variant['count']}x {item.title} {variant['type']} - ${variant['price']}"
            c.drawString(10, y_position, text)
            y_position -= 15

    # Totales
    y_position -= 10
    c.setFont("Helvetica", 10)
    if order_data.shipping == "delivery":
        c.drawString(10, y_position, f"Envío: ${order_data.priceDelivery}")
        y_position -= 15
    if order_data.appliedDiscount > 0:
        c.drawString(10, y_position, f"Descuento: ${order_data.appliedDiscount}")
        y_position -= 15

    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - 10, y_position, f"Total: ${order_data.totalAmmount}")
    y_position -= 20

    # Mensaje de agradecimiento
    c.drawCentredString(width / 2, y_position, "Gracias por su compra")
    c.showPage()
    c.save()

    return file_name

# Función para enviar a imprimir en Windows
def send_to_printer(file_path: str, printer_name: str):
    try:
        # Verificar que la impresora existe
        printer_handle = win32print.OpenPrinter(printer_name)
        printer_info = win32print.GetPrinter(printer_handle, 2)
        printer_status = printer_info["Status"]

        if printer_status != 0:
            return {"error": "La impresora no está disponible"}

        # Método alternativo: Usar el visor de PDF de Windows para imprimir
        os.startfile(file_path, "print")

        return {"status": "Impresión enviada con éxito"}
    except Exception as e:
        return {"error": f"Error al imprimir: {e}"}

# Endpoint para generar e imprimir el ticket
@app.post("/print_ticket/")
async def print_ticket(order_data: OrderData):
    ticket_path = generate_ticket(order_data)
    print(ticket_path)
    print_status = send_to_printer(ticket_path, order_data.printer_name)
    return {"message": "Ticket generado e impresión enviada", "printer_status": print_status, "printer_name": order_data.printer_name}

@app.get("/list_printers/")
async def list_printers():
    try:
        printers = []
        printer_info = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)

        for printer in printer_info:
            printers.append(printer[2])  # El nombre de la impresora está en la posición 2

        return {"printers": printers}

    except Exception as e:
        return {"error": f"Error al obtener la lista de impresoras: {str(e)}"}
import win32print
from fastapi import FastAPI

app = FastAPI()

# Diccionario de estados de la impresora en Windows
PRINTER_STATUS = {
    0: "Disponible",
    1: "Error",
    2: "Offline",
    3: "Papel agotado",
    4: "Papel atascado",
    5: "Imprimiendo",
    6: "Pausada",
    7: "En espera"
}

@app.get("/printer_status/")
async def printer_status(printer_name: str):
    try:
        # Intentar abrir la impresora
        printer_handle = win32print.OpenPrinter(printer_name)
        printer_info = win32print.GetPrinter(printer_handle, 2)  # Nivel 2 para más información

        # Extraer el estado de la impresora
        status_code = printer_info["Status"]
        printer_status = PRINTER_STATUS.get(status_code, f"Estado desconocido ({status_code})")

        # Extraer el puerto de la impresora (si está en "NULO", la impresora no está conectada)
        port_name = printer_info["pPortName"]
        if port_name.lower() == "nul" or not port_name:
            printer_status = "No conectada"

        # Extraer cantidad de trabajos en cola
        print_jobs = printer_info["cJobs"]

        # Cerrar el handle de la impresora
        win32print.ClosePrinter(printer_handle)

        return {
            "printer_name": printer_info["pPrinterName"],
            "status": printer_status,
            "driver_name": printer_info["pDriverName"],
            "port_name": port_name,
            "print_jobs": print_jobs
        }

    except Exception as e:
        return {"error": f"No se pudo obtener el estado de la impresora '{printer_name}': {str(e)}"}
