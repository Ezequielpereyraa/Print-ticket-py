from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

def generate_ticket(order_data):
    # Calcular la altura del ticket dinámicamente
    base_height = 100  # Altura base en mm
    line_height = 20  # Altura de cada línea en mm
    num_lines = 10 + sum(len(item['variants']) for item in order_data['order'])  # Líneas fijas + líneas por variantes
    height = (base_height + num_lines * line_height) * mm

    # Configuración del tamaño del ticket (58mm de ancho)
    width = 58 * mm
    c = canvas.Canvas("ticket.pdf", pagesize=(width, height))

    # Información del ticket
    c.setFont("Helvetica", 10)
    y_position = height - 20
    c.drawString(10, y_position, f"Pedido ID: {order_data['pedidoId']}")
    y_position -= 20
    c.drawString(10, y_position, f"Cliente: {order_data['name']}")
    y_position -= 20
    c.drawString(10, y_position, f"Fecha: {order_data['date']}")
    y_position -= 20
    c.drawString(10, y_position, f"Dirección: {order_data['address']}")
    y_position -= 20
    c.drawString(10, y_position, f"Referencia: {order_data['addressReference']}")
    y_position -= 20
    c.drawString(10, y_position, f"Teléfono: {order_data['ws']}")
    y_position -= 20
    c.drawString(10, y_position, f"Nota: {order_data['note']}")
    y_position -= 20
    c.drawString(10, y_position, f"Envío: {order_data['shipping']}")
    y_position -= 20
    c.drawString(10, y_position, f"Hora: {order_data['hour']}")
    y_position -= 20
    c.drawString(10, y_position, f"Pago: {order_data['payment']}")
    y_position -= 20

    # Detalles de la orden
    for item in order_data['order']:
        c.drawString(10, y_position, f"Producto: {item['title']}")
        y_position -= 20
        for variant in item['variants']:
            c.drawString(20, y_position, f"Tipo: {variant['type']}, Cantidad: {variant['count']}, Precio: ${variant['price']}")
            y_position -= 20

    # Totales
    c.drawString(10, y_position, f"Total sin descuento: ${order_data['totalWithoutDiscount']}")
    y_position -= 20
    c.drawString(10, y_position, f"Descuento aplicado: ${order_data['appliedDiscount']}")
    y_position -= 20
    c.drawString(10, y_position, f"Total: ${order_data['totalAmmount']}")
    y_position -= 20
    c.drawString(10, y_position, f"Precio de envío: ${order_data['priceDelivery']}")

    # Finalizar el PDF
    c.showPage()
    c.save()

# Ejemplo de uso
if __name__ == "__main__":
    order_data = {
        "address": "Varela Ortiz 2375",
        "paymentAmmount": "",
        "totalWithoutDiscount": 9000,
        "addressReference": "Casa reja negras",
        "appliedDiscount": 0,
        "dt_create": "5/1/2025",
        "date": "05/01/2025",
        "shipping": "delivery",
        "hour": "23:59",
        "payment": "transfer",
        "dt_done": None,
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
        "dt_confirm": None,
        "note": "SIN TOMATE",
        "name": "Ignacio Rueda",
        "totalAmmount": 9800,
        "quantityPotatos": "",
        "ws": "3517877942",
        "priceDelivery": 800,
        "status": "DELETED",
        "id": "3VgfuW9G1DLKNsYxfIEQ"
    }
    generate_ticket(order_data)
