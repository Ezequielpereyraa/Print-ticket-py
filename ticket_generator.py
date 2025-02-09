import os
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def generate_ticket(order_data):
    # Ajustar la altura del ticket basado en el contenido real
    content_height = 10
    content_height += 5 * 5  # Información del ticket (5 líneas)
    content_height += 10 * sum(len(item['variants']) for item in order_data['order'])  # Detalles de la orden
    if order_data['shipping'] == "delivery":
        content_height += 20  # Envío
    if order_data['appliedDiscount'] > 0:
        content_height += 20  # Descuento aplicado
    content_height += 20  # Total
    content_height += 20  # Agradecimiento

    height = content_height * mm

    # Configuración del tamaño del ticket (58mm de ancho)
    width = 58 * mm
    c = canvas.Canvas("ticket.pdf", pagesize=(width, height))

    # Título centrado
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 20, "Freakys Burgers")
    y_position = height - 40

    # Información del ticket
    c.setFont("Helvetica", 10)
    wrap_and_draw_text(c, order_data['name'], 10, y_position, width - 20, "Helvetica", 10)
    y_position -= 20
    wrap_and_draw_text(c, order_data['date'], 10, y_position, width - 20, "Helvetica", 10)
    y_position -= 20
    wrap_and_draw_text(c, order_data['address'], 10, y_position, width - 20, "Helvetica", 10)
    y_position -= 20
    wrap_and_draw_text(c, order_data['addressReference'], 10, y_position, width - 20, "Helvetica", 10)
    y_position -= 20
    wrap_and_draw_text(c, order_data['ws'], 10, y_position, width - 20, "Helvetica", 10)
    y_position -= 20
    c.setFont("Helvetica-Bold", 10)
    wrap_and_draw_text(c, order_data['note'], 10, y_position, width - 20, "Helvetica-Bold", 10)
    c.setFont("Helvetica", 10)
    y_position -= 20

    # Detalles de la orden
    y_position -= 10  # Margen superior
    c.setFont("Helvetica-Bold", 10)
    c.drawString(10, y_position, "Detalles del Pedido")
    c.setFont("Helvetica", 8)  # Reducir el tamaño de la fuente
    y_position -= 20
    for item in order_data['order']:
        for variant in item['variants']:
            text = f"{variant['count']}x {item['title']} {variant['type']} $ {variant['price']}"
            text_width = c.stringWidth(text, "Helvetica", 8)
            if text_width > width - 20:
                lines = wrap_text(text, width - 20, "Helvetica", 8)
                for line in lines:
                    c.drawString(10, y_position, line)
                    y_position -= 10
            else:
                c.drawString(10, y_position, text)
                y_position -= 20
    y_position -= 10  # Margen inferior

    # Totales
    if order_data['shipping'] == "delivery":
        c.drawString(10, y_position, f"Envío: ${order_data['priceDelivery']}")
        y_position -= 20
    if order_data['appliedDiscount'] > 0:
        c.drawString(10, y_position, f"Descuento aplicado: ${order_data['appliedDiscount']}")
        y_position -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - 10, y_position, f"Total: ${order_data['totalAmmount']}")
    y_position -= 20

    # Mensaje de agradecimiento
    c.drawCentredString(width / 2, y_position, "Gracias por su compra")

    # Finalizar el PDF
    c.showPage()
    c.save()

    # Enviar a imprimir
    send_to_printer("./ticket.pdf", "Comandera")

def send_to_printer(file_path, printer_name):
    if not file_path or not os.path.exists(file_path):
        raise ValueError("No se envió ningún archivo.")
    if not printer_name:
        raise ValueError("No se ingresó nombre de impresora")

    try:
        from escpos.printer import Usb
        from PyPDF2 import PdfReader
        import tempfile

        # Cargar el PDF
        pdf_document = PdfReader(open(file_path, "rb"))

        # Crear una impresora USB
        # Asegúrate de reemplazar `idVendor` y `idProduct` con los valores correctos para tu impresora
        printer = Usb(idVendor=0x04b8, idProduct=0x0e15)  # Ejemplo de valores, actualiza según tu impresora

        # Imprimir cada página del PDF
        for page_num in range(len(pdf_document.pages)):
            page = pdf_document.pages[page_num]
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
                page_image = page.to_image()
                page_image.save(temp_image.name)
                printer.image(temp_image.name)
                os.remove(temp_image.name)

        printer.cut()

    except Exception as e:
        raise RuntimeError(f"Error al imprimir el PDF: {e}")

def wrap_text(text, max_width, font_name, font_size):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        if current_line:
            test_line = f"{current_line} {word}"
        else:
            test_line = word
        if pdfmetrics.stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def wrap_and_draw_text(c, text, x, y, max_width, font_name, font_size):
    lines = wrap_text(text, max_width, font_name, font_size)
    for line in lines:
        c.drawString(x, y, line)
        y -= 10
