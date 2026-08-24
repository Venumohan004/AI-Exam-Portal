import os

from django.conf import settings

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    HRFlowable,
)


def build_result_pdf(buffer, attempt):

    # ==================================================
    # COLORS
    # ==================================================

    DARK_BLUE = HexColor("#12355B")
    GOLD = HexColor("#D4AF37")
    LIGHT_BLUE = HexColor("#EAF2F8")
    LIGHT_GRAY = HexColor("#F5F7FA")
    GREEN = HexColor("#198754")
    DARK_GRAY = HexColor("#343A40")
    GRAY = HexColor("#6C757D")
    WHITE = colors.white
    BORDER = HexColor("#D9E1E8")

    # ==================================================
    # DOCUMENT
    # ==================================================

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=35,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    elements = []

    # ==================================================
    # LOGO
    # ==================================================

    logo_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "Ai_exam_portal_logo.avif"
    )

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=55,
            height=55
        )

        logo_table = Table(
            [[logo]],
            colWidths=[doc.width]
        )

        logo_table.setStyle(
            TableStyle([
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
            ])
        )

        elements.append(logo_table)

        elements.append(
            Spacer(1, 6)
        )

    # ==================================================
    # HEADER
    # ==================================================

    title_style = ParagraphStyle(
        "MainTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=27,
        alignment=TA_CENTER,
        textColor=DARK_BLUE,
        spaceAfter=4,
    )

    elements.append(
        Paragraph(
            "AI EXAM PORTAL",
            title_style
        )
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        alignment=TA_CENTER,
        textColor=GOLD,
    )

    elements.append(
        Paragraph(
            "EXAMINATION RESULT REPORT",
            subtitle_style
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    elements.append(
        HRFlowable(
            width="100%",
            thickness=2,
            color=GOLD,
            spaceBefore=2,
            spaceAfter=15,
        )
    )

    # ==================================================
    # RESULT INFORMATION
    # ==================================================

    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=DARK_BLUE,
        alignment=TA_LEFT,
        spaceAfter=8,
    )

    elements.append(
        Paragraph(
            "STUDENT & EXAM DETAILS",
            section_style
        )
    )

    # ==================================================
    # DETAILS TABLE
    # ==================================================

    student_name = attempt.student.username
    exam_title = attempt.exam.title
    subject = attempt.exam.subject

    details_data = [

        [
            Paragraph(
                "<b>Student Name</b>",
                styles["Normal"]
            ),
            Paragraph(
                str(student_name),
                styles["Normal"]
            ),
        ],

        [
            Paragraph(
                "<b>Exam</b>",
                styles["Normal"]
            ),
            Paragraph(
                str(exam_title),
                styles["Normal"]
            ),
        ],

        [
            Paragraph(
                "<b>Subject</b>",
                styles["Normal"]
            ),
            Paragraph(
                str(subject),
                styles["Normal"]
            ),
        ],

        [
            Paragraph(
                "<b>Submitted</b>",
                styles["Normal"]
            ),
            Paragraph(
                attempt.submitted_at.strftime(
                    "%d %B %Y • %I:%M %p"
                ),
                styles["Normal"]
            ),
        ],
    ]

    details_table = Table(
        details_data,
        colWidths=[
            1.55 * inch,
            5.35 * inch
        ],
        hAlign="CENTER",
    )

    details_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                LIGHT_BLUE
            ),

            (
                "BACKGROUND",
                (1, 0),
                (1, -1),
                WHITE
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (0, -1),
                DARK_BLUE
            ),

            (
                "TEXTCOLOR",
                (1, 0),
                (1, -1),
                DARK_GRAY
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (1, 0),
                (1, -1),
                "Helvetica"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                10
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                12
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                12
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.6,
                BORDER
            ),
        ])
    )

    elements.append(details_table)

    elements.append(
        Spacer(1, 20)
    )

    # ==================================================
    # PERFORMANCE SUMMARY
    # ==================================================

    elements.append(
        Paragraph(
            "PERFORMANCE SUMMARY",
            section_style
        )
    )

    status = "PASS" if attempt.is_passed else "FAIL"

    status_color = GREEN if attempt.is_passed else HexColor("#DC3545")

    performance_data = [

        [
            Paragraph(
                "<b>SCORE</b>",
                ParagraphStyle(
                    "ScoreHeader",
                    alignment=TA_CENTER,
                    textColor=DARK_BLUE,
                    fontName="Helvetica-Bold",
                    fontSize=9,
                )
            ),

            Paragraph(
                "<b>PERCENTAGE</b>",
                ParagraphStyle(
                    "PercentageHeader",
                    alignment=TA_CENTER,
                    textColor=DARK_BLUE,
                    fontName="Helvetica-Bold",
                    fontSize=9,
                )
            ),

            Paragraph(
                "<b>STATUS</b>",
                ParagraphStyle(
                    "StatusHeader",
                    alignment=TA_CENTER,
                    textColor=DARK_BLUE,
                    fontName="Helvetica-Bold",
                    fontSize=9,
                )
            ),
        ],

        [
            Paragraph(
                f"<b>{attempt.score}</b> / {attempt.total_marks}",
                ParagraphStyle(
                    "ScoreValue",
                    alignment=TA_CENTER,
                    textColor=DARK_BLUE,
                    fontName="Helvetica-Bold",
                    fontSize=19,
                )
            ),

            Paragraph(
                f"<b>{attempt.percentage}%</b>",
                ParagraphStyle(
                    "PercentageValue",
                    alignment=TA_CENTER,
                    textColor=DARK_BLUE,
                    fontName="Helvetica-Bold",
                    fontSize=19,
                )
            ),

            Paragraph(
                f"<b>{status}</b>",
                ParagraphStyle(
                    "StatusValue",
                    alignment=TA_CENTER,
                    textColor=status_color,
                    fontName="Helvetica-Bold",
                    fontSize=19,
                )
            ),
        ],
    ]

    performance_table = Table(
        performance_data,
        colWidths=[
            2.3 * inch,
            2.3 * inch,
            2.3 * inch,
        ],
        rowHeights=[
            25,
            45,
        ],
        hAlign="CENTER",
    )

    performance_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                LIGHT_GRAY
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.8,
                BORDER
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
        ])
    )

    elements.append(
        performance_table
    )

    elements.append(
        Spacer(1, 20)
    )

    # ==================================================
    # RESULT MESSAGE
    # ==================================================

    message_style = ParagraphStyle(
        "Message",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=DARK_BLUE,
    )

    message = (
        "Congratulations! You have successfully completed "
        "the examination."
        if attempt.is_passed
        else
        "Thank you for completing the examination."
    )

    elements.append(
        Paragraph(
            message,
            message_style
        )
    )

    elements.append(
        Spacer(1, 25)
    )

    # ==================================================
    # SIGNATURE SECTION
    # ==================================================

    signature_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "sig-no-bg.png"
    )

    if os.path.exists(signature_path):

        signature = Image(
            signature_path,
            width=1.55 * inch,
            height=0.50 * inch
        )

        signature_block = Table(
            [
                [signature],
                ["____________________________"],
                ["Exam Administrator"],
                ["Authorized Signature • AI Exam Portal"],
            ],
            colWidths=[2.2 * inch],
            hAlign="RIGHT",
        )

        signature_block.setStyle(
            TableStyle([

                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "FONTNAME",
                    (0, 1),
                    (0, 1),
                    "Helvetica"
                ),

                (
                    "FONTNAME",
                    (0, 2),
                    (0, 2),
                    "Helvetica-Bold"
                ),

                (
                    "FONTNAME",
                    (0, 3),
                    (0, 3),
                    "Helvetica"
                ),

                (
                    "FONTSIZE",
                    (0, 1),
                    (0, 1),
                    8
                ),

                (
                    "FONTSIZE",
                    (0, 2),
                    (0, 2),
                    9
                ),

                (
                    "FONTSIZE",
                    (0, 3),
                    (0, 3),
                    7
                ),

                (
                    "TEXTCOLOR",
                    (0, 2),
                    (0, 2),
                    DARK_BLUE
                ),

                (
                    "TEXTCOLOR",
                    (0, 3),
                    (0, 3),
                    GRAY
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    1
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    1
                ),
            ])
        )

        elements.append(
            signature_block
        )

    elements.append(
        Spacer(1, 20)
    )

    # ==================================================
    # FOOTER
    # ==================================================

    elements.append(
        HRFlowable(
            width="100%",
            thickness=0.7,
            color=BORDER,
            spaceBefore=5,
            spaceAfter=8,
        )
    )

    certificate_id = (
        f"RESULT-"
        f"{attempt.submitted_at.strftime('%Y%m%d')}-"
        f"{attempt.id:04d}"
    )

    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=GRAY,
    )

    elements.append(
        Paragraph(
            f"Result ID: {certificate_id}<br/>"
            "This result report is digitally generated and verified by AI Exam Portal.",
            footer_style
        )
    )

    # ==================================================
    # BUILD PDF
    # ==================================================

    doc.build(elements)