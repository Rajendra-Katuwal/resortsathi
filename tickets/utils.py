from io import BytesIO
import qrcode
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def generate_qr_code(data: str) -> ImageReader:
    qr_img = qrcode.make(data)
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer)
    qr_buffer.seek(0)
    return ImageReader(qr_buffer)

def generate_standard_ticket_pdf(ticket, data_list):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(80 * mm, 130 * mm))  # standard ticket size

    qr_data = f"Ticket ID: {ticket.ticket_id}\nIssued: {ticket.issued_at.strftime('%Y-%m-%d')}"
    qr_image = generate_qr_code(qr_data)

    for item in data_list:
        # HEADER
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(40 * mm, 124 * mm, "Godawari River Side Resort")
        c.setFont("Helvetica", 9)
        c.drawCentredString(40 * mm, 119 * mm, "Sundarharaincha-4, Morang")
        c.drawCentredString(40 * mm, 114 * mm, f"Date: {item['issued_at']}")

        # TICKET TYPE
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(40 * mm, 105 * mm, ticket.template.name)

        # SUBTITLE
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(40 * mm, 100 * mm, "Valid for single use by one individual only.")

        # PRICE AND PAYMENT
        c.setFont("Helvetica", 8)
        c.drawString(10 * mm, 90 * mm, "Price:")
        c.drawString(25 * mm, 90 * mm, f"Rs. {ticket.template.price}/-")
        c.drawString(10 * mm, 85 * mm, "Payment Medium:")
        c.drawString(40 * mm, 85 * mm, ticket.get_payment_mode_display())

        # QR CODE - centered, with margin
        qr_x = 25 * mm
        qr_y = 42 * mm
        qr_size = 30 * mm
        c.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size)

        # NOTES - placed *below* QR code
        c.setFont("Helvetica", 6)
        c.drawString(10 * mm, 35 * mm, "Note: Kindly ensure to request a physical bill for VAT refund purposes.")
        c.drawString(10 * mm, 31 * mm, "This copy is intended for internal reference only.")

        # FOOTER
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(40 * mm, 15 * mm, "Powered by: Resort Sathi")
        c.setFont("Helvetica", 7)
        c.drawCentredString(40 * mm, 10 * mm, "www.resortsathi.com")

        c.showPage()

    c.save()
    buffer.seek(0)
    return buffer



def generate_ticket_pdf(ticket, data_list):
    template_map = {
        'Standard': generate_standard_ticket_pdf,
        # add other template handlers here as needed
    }
    func = template_map.get(ticket.template.name, generate_standard_ticket_pdf)
    return func(ticket, data_list)
