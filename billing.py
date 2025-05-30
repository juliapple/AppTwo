from reportlab.pdfgen import canvas

def calculate_parking_fee(category, days):
    free_days = 50 if category in ['Full Town', 'Full Town Family'] else 40
    paid_days = max(0, days - free_days)
    if paid_days <= 50:
        return paid_days * 15
    else:
        return (50 * 15) + ((paid_days - 50) * 20)

def generate_invoice_pdf(member_name, amount):
    file_name = f"Invoice_{member_name}.pdf"
    c = canvas.Canvas(file_name)
    c.drawString(100, 750, f"Invoice for {member_name}")
    c.drawString(100, 730, f"Amount Due: €{amount}")
    c.save()
