from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_pdf_report(user_email: str, predictions: list):
    report_folder = "uploads/reports"
    os.makedirs(report_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"{user_email.replace('@', '_')}_report_{timestamp}.pdf"
    pdf_path = os.path.join(report_folder, pdf_filename)

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, f"CerviCare AI Prediction Report")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"User: {user_email}")
    c.drawString(50, height - 85, f"Generated: {timestamp}")

    c.drawString(50, height - 110, "Results:")
    y = height - 130

    for i, row in enumerate(predictions[:10]):  # Limit rows for layout
        line = f"#{i+1} → Age: {row.get('age')}, Smoking: {row.get('smoking')}, HPV: {row.get('hpv_result')}, Risk: {row.get('prediction')}"
        c.drawString(60, y, line)
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
    return f"/{pdf_path}"
