from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generate_ticket(order_data):
    # Ajustar la altura del ticket basado en el contenido real
    content_height = 0
    content_height += 10 * 5  # Información del ticket (5 líneas)
    content_height += 10 * sum(len(item['variants']) for item in order_data['order'])  # Detalles de la orden
    if order_data['shipping'] == "delivery":
        content_height += 20  # Envío
    if order_data['appliedDiscount'] > 0:
        content_height += 20  # Descuento aplicado
    content_height += 20  # Total

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
    c.drawString(10, y_position, f"{order_data['name']}")
    y_position -= 20
    c.drawString(10, y_position, f"{order_data['date']}")
    y_position -= 20
    c.drawString(10, y_position, f"{order_data['address']}")
    y_position -= 20
    c.drawString(10, y_position, f"{order_data['addressReference']}")
    y_position -= 20
    c.drawString(10, y_position, f"{order_data['ws']}")
    y_position -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(10, y_position, f"{order_data['note']}")
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
            c.drawString(10, y_position, f"{variant['count']}x {item['title']} {variant['type']} $ {variant['price']}")
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

# Ejemplo de uso
if __name__ == "__main__":
    order_data = {
        "address": "Varela Ortiz 2375",
        "totalWithoutDiscount": 9000,
        "addressReference": "Casa reja negras",
        "appliedDiscount": 0,
        "date": "05/01/2025",
        "shipping": "delivery",
        "payment": "transfer",
        "order": [
            {
                "variants": [
                    {
                        "count": 1,
                        "price": 8500,
                        "type": "triple",
                        "showType": True
                    }
                ],
                "title": "American",
                "id": 1011
            },
            {
                "title": "Pote de Creamy Bliss",
                "variants": [
                    {
                        "price": 500,
                        "type": "simple",
                        "showType": False,
                        "count": 1
                    }
                ],
                "id": 504
            }
        ],
        "pedidoId": "ZSBZ3",
        "note": "SIN TOMATE",
        "name": "Ignacio Rueda",
        "totalAmmount": 9800,
        "ws": "3517877942",
        "priceDelivery": 800,
    }
    generate_ticket(order_data)
