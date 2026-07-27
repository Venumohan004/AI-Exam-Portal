from reportlab.lib.colors import HexColor
from reportlab.lib.colors import (
    HexColor,
    gold,
    darkblue,
    black,
)
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas


import os
from django.conf import settings

def build_certificate_pdf(buffer, attempt):
    """
    Generate a certificate PDF for a passed student.
    """
    pdf = canvas.Canvas(
        buffer,
        pagesize=landscape(A4)
    )

    width, height = landscape(A4)

    # ==================================================
    # Background
    # ==================================================

    pdf.setFillColor(HexColor("#F8F9FA"))

    pdf.rect(
        0,
        0,
        width,
        height,
        fill=1,
        stroke=0
    )

    # ==================================================
    # Double Border
    # ==================================================

    pdf.setStrokeColor(gold)

    pdf.setLineWidth(5)

    pdf.rect(
        20,
        20,
        width - 40,
        height - 40
    )

    pdf.setStrokeColor(darkblue)

    pdf.setLineWidth(2)

    pdf.rect(
        35,
        35,
        width - 70,
        height - 70
    )

    # ==================================================
    # Logo
    # ==================================================

    logo_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "logo.png"
    )

    if os.path.exists(logo_path):

        pdf.drawImage(
            logo_path,
            width / 2 - 40,
            height - 120,
            width=80,
            height=80,
            mask="auto"
        )

    # ==================================================
    # Portal Name
    # ==================================================

    pdf.setFont(
        "Helvetica-Bold",
        26
    )

    pdf.setFillColor(
        darkblue
    )

    pdf.drawCentredString(
        width / 2,
        height - 145,
        "AI EXAM PORTAL"
    )

    # ==================================================
    # Certificate Heading
    # ==================================================

    pdf.setFont(
        "Helvetica-Bold",
        30
    )

    pdf.setFillColor(
        gold
    )

    pdf.drawCentredString(
        width / 2,
        height - 185,
        "CERTIFICATE OF COMPLETION"
    )
    pdf.line(
    120,
    height-210,
    width-120,
    height-210
    )

    # ==================================================
    # Decorative Line
    # ==================================================

    pdf.setStrokeColor(
        gold
    )

    pdf.setLineWidth(2)

    pdf.line(
        180,
        height - 200,
        width - 180,
        height - 200
    )

    # ==================================================
    # Certificate Text
    # ==================================================

    pdf.setFillColor(
        black
    )

    pdf.setFont(
        "Helvetica",
        16
    )

    pdf.drawCentredString(
        width / 2,
        height - 250,
        "This certificate is proudly presented to"
    )

    # ==================================================
    # Student Name
    # ==================================================

    pdf.setFont(
        "Helvetica-Bold",
        40
    )

    pdf.setFillColor(
        HexColor("#198754")
    )

    pdf.drawCentredString(
        width / 2,
        height - 300,
        attempt.student.username.upper()
    )

    # ==================================================
    # Completed Text
    # ==================================================

    pdf.setFillColor(
        black
    )

    pdf.setFont(
        "Helvetica",
        16
    )

    pdf.drawCentredString(
        width / 2,
        height - 340,
        "For successfully completing"
    )

    # ==================================================
    # Exam Title
    # ==================================================

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.setFillColor(
        darkblue
    )

    pdf.drawCentredString(
        width / 2,
        height - 375,
        attempt.exam.title
    )
    # ==================================================
    # Subject
    # ==================================================

    pdf.setFillColor(black)

    pdf.setFont(
        "Helvetica",
        15
    )

    pdf.drawCentredString(
        width / 2,
        height - 410,
        f"Subject : {attempt.exam.subject}"
    )

    # ==================================================
    # Score
    # ==================================================

    pdf.drawCentredString(
        width / 2,
        height - 435,
        f"Score : {attempt.score} / {attempt.total_marks}"
    )

    # ==================================================
    # Percentage
    # ==================================================

    pdf.drawCentredString(
        width / 2,
        height - 470,
        f"Percentage : {attempt.percentage}%"
    )

    # ==================================================
    # PASS Status
    # ==================================================

    pdf.setFillColor(
        HexColor("#198754")
    )

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawCentredString(
        width / 2,
        height - 490,
        "RESULT : PASS"
    )

    # ==================================================
    # Date
    # ==================================================

    pdf.setFillColor(
        black
    )

    pdf.setFont(
        "Helvetica",
        14
    )

    pdf.drawCentredString(
        width / 2,
        height - 515,
        f"Date : {attempt.submitted_at.strftime('%d %B %Y')}"
    )

    # ==================================================
    # Certificate ID
    # ==================================================

    certificate_id = (
        f"CERT-"
        f"{attempt.submitted_at.strftime('%Y%m%d')}-"
        f"{attempt.id:04d}"
    )

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawCentredString(
        width / 2,
        height - 540,
        f"Certificate ID : {certificate_id}"
    )
    # ==================================================
    # VERIFIED GOLD SEAL
    # ==================================================

    seal_x = 130
    seal_y = 85

    pdf.setFillColor(gold)
    pdf.circle(
        seal_x,
        seal_y,
        45,
        fill=1
    )

    pdf.setStrokeColor(darkblue)
    pdf.setLineWidth(2)
    pdf.circle(
        seal_x,
        seal_y,
        45
    )

    pdf.setFillColor(black)

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawCentredString(
        seal_x,
        seal_y + 10,
        "★★★★★"
    )

    pdf.drawCentredString(
        seal_x,
        seal_y - 2,
        "VERIFIED"
    )

    pdf.drawCentredString(
        seal_x,
        seal_y - 14,
        "★★★★★"
    )

    # ==================================================
    # Congratulations
    # ==================================================

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.setFillColor(
        darkblue
    )

    pdf.drawCentredString(
        width / 2,
        145,
        "Congratulations on successfully completing the examination with excellent performance."
    )

    # ==================================================
    # Signature Line
    # ==================================================

    pdf.setStrokeColor(black)

    pdf.setLineWidth(1)

    pdf.line(
        width - 260,
        90,
        width - 90,
        90
    )

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawCentredString(
        width - 175,
        75,
        "Exam Administrator"
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawCentredString(
        width - 175,
        55,
        "AI Exam Portal"
    )

    # ==================================================
    # Footer
    # ==================================================

    pdf.setFont(
        "Helvetica-Oblique",
        10
    )
    pdf.setFont(
            "Helvetica-Bold",
            8
        )
    pdf.setFillColor(
        HexColor("#666666")
    )

    pdf.drawCentredString(
        width / 2,
        25,
        "This certificate is digitally verified and generated by AI Exam Portal."
    )

    # ==================================================
    # Save PDF
    # ==================================================

    pdf.showPage()

    pdf.save()

   
    