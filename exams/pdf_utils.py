import os

from django.conf import settings

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    HRFlowable,
    PageBreak,
    KeepTogether,
)


# ============================================================
# PROFESSIONAL EXAM RESULT PDF
# ============================================================

def build_result_pdf(buffer, attempt):

    # ========================================================
    # COLORS
    # ========================================================

    DARK_BLUE = HexColor("#12355B")
    GOLD = HexColor("#D4AF37")

    LIGHT_BLUE = HexColor("#EAF2F8")
    LIGHT_GRAY = HexColor("#F5F7FA")

    GREEN = HexColor("#198754")
    RED = HexColor("#DC3545")
    ORANGE = HexColor("#F59E0B")

    DARK_GRAY = HexColor("#343A40")
    GRAY = HexColor("#6C757D")

    WHITE = colors.white
    BORDER = HexColor("#D9E1E8")

    # ========================================================
    # DOCUMENT
    # ========================================================

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,

        rightMargin=40,
        leftMargin=40,
        topMargin=55,
        bottomMargin=55,
    )

    styles = getSampleStyleSheet()

    elements = []

    # ========================================================
    # CUSTOM STYLES
    # ========================================================

    title_style = ParagraphStyle(
        "MainTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        textColor=DARK_BLUE,
        spaceAfter=3,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=GOLD,
        spaceAfter=5,
    )

    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=DARK_BLUE,
        alignment=TA_LEFT,
        spaceBefore=2,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=DARK_GRAY,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=normal_style,
        fontSize=8,
        leading=10,
    )

    center_style = ParagraphStyle(
        "Center",
        parent=normal_style,
        alignment=TA_CENTER,
    )

    question_style = ParagraphStyle(
        "Question",
        parent=normal_style,
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=DARK_BLUE,
        spaceAfter=5,
    )

    explanation_style = ParagraphStyle(
        "Explanation",
        parent=normal_style,
        fontSize=8.5,
        leading=12,
        textColor=DARK_GRAY,
    )

    # ========================================================
    # DATA
    # ========================================================

    student_name = str(
        attempt.student.username
    )

    exam_title = str(
        attempt.exam.title
    )

    subject = str(
        attempt.exam.subject
    )

    difficulty = str(
        attempt.exam.difficulty
    )

    duration = str(
        attempt.exam.duration_minutes
    )

    # ========================================================
    # SUBMITTED DATE
    # ========================================================

    if attempt.submitted_at:

        submitted = attempt.submitted_at.strftime(
            "%d %B %Y • %I:%M %p"
        )

    else:

        submitted = "N/A"

    # ========================================================
    # ANSWERS
    # ========================================================

    answers = list(
        attempt.answers
        .select_related(
            "question",
            "selected_option",
        )
        .prefetch_related(
            "question__options",
        )
        .order_by(
            "question__question_number"
        )
    )

    # ========================================================
    # PERFORMANCE CALCULATION
    # ========================================================

    correct = 0
    wrong = 0
    unanswered = 0
    negative_marks = 0

    for answer in answers:

        if answer.selected_option is None:

            unanswered += 1

        elif answer.selected_option.is_correct:

            correct += 1

        else:

            wrong += 1

            if answer.marks_awarded < 0:

                negative_marks += abs(
                    answer.marks_awarded
                )

    total_questions = attempt.exam.questions.count()

    # Safety correction
    unanswered = max(
        0,
        total_questions - correct - wrong
    )

    # ========================================================
    # TIME TAKEN
    # ========================================================

    if (
        attempt.started_at
        and attempt.submitted_at
    ):

        time_taken = round(
            (
                attempt.submitted_at
                - attempt.started_at
            ).total_seconds()
            / 60,
            2,
        )

    else:

        time_taken = 0

    # ========================================================
    # STATUS
    # ========================================================

    if attempt.is_passed:

        status = "PASS"
        status_color = GREEN

    else:

        status = "FAIL"
        status_color = RED

    # ========================================================
    # HEADER FUNCTION
    # ========================================================

    def draw_header_footer(
        canvas,
        document,
    ):

        canvas.saveState()

        # ----------------------------------------------------
        # TOP LINE
        # ----------------------------------------------------

        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(1.5)

        canvas.line(
            40,
            letter[1] - 35,
            letter[0] - 40,
            letter[1] - 35,
        )

        # ----------------------------------------------------
        # HEADER TEXT
        # ----------------------------------------------------

        canvas.setFont(
            "Helvetica-Bold",
            8,
        )

        canvas.setFillColor(
            DARK_BLUE
        )

        canvas.drawString(
            40,
            letter[1] - 27,
            "AI EXAM PORTAL",
        )

        canvas.setFont(
            "Helvetica",
            7,
        )

        canvas.setFillColor(
            GRAY
        )

        canvas.drawRightString(
            letter[0] - 40,
            letter[1] - 27,
            "Examination Result Report",
        )

        # ----------------------------------------------------
        # FOOTER LINE
        # ----------------------------------------------------

        canvas.setStrokeColor(
            BORDER
        )

        canvas.setLineWidth(
            0.6
        )

        canvas.line(
            40,
            35,
            letter[0] - 40,
            35,
        )

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        canvas.setFont(
            "Helvetica",
            7,
        )

        canvas.setFillColor(
            GRAY
        )

        canvas.drawString(
            40,
            23,
            "AI Exam Portal • Digitally Generated Result",
        )

        canvas.drawRightString(
            letter[0] - 40,
            23,
            f"Page {document.page}",
        )

        canvas.restoreState()

    # ========================================================
    # LOGO
    # ========================================================

    logo_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "Ai_exam_portal_logo.avif",
    )

    if os.path.exists(logo_path):

        try:

            logo = Image(
                logo_path,
                width=55,
                height=55,
            )

            logo_table = Table(
                [[logo]],
                colWidths=[
                    doc.width
                ],
            )

            logo_table.setStyle(
                TableStyle([
                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER",
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                ])
            )

            elements.append(
                logo_table
            )

            elements.append(
                Spacer(1, 4)
            )

        except Exception:
            pass

    # ========================================================
    # MAIN HEADER
    # ========================================================

    elements.append(
        Paragraph(
            "AI EXAM PORTAL",
            title_style,
        )
    )

    elements.append(
        Paragraph(
            "EXAMINATION RESULT REPORT",
            subtitle_style,
        )
    )

    elements.append(
        HRFlowable(
            width="100%",
            thickness=2,
            color=GOLD,
            spaceBefore=3,
            spaceAfter=15,
        )
    )

    # ========================================================
    # STUDENT & EXAM DETAILS
    # ========================================================

    elements.append(
        Paragraph(
            "STUDENT & EXAM DETAILS",
            section_style,
        )
    )

    details_data = [

        [
            Paragraph(
                "<b>Student Name</b>",
                normal_style,
            ),
            Paragraph(
                student_name,
                normal_style,
            ),
        ],

        [
            Paragraph(
                "<b>Exam</b>",
                normal_style,
            ),
            Paragraph(
                exam_title,
                normal_style,
            ),
        ],

        [
            Paragraph(
                "<b>Subject</b>",
                normal_style,
            ),
            Paragraph(
                subject,
                normal_style,
            ),
        ],

        [
            Paragraph(
                "<b>Difficulty</b>",
                normal_style,
            ),
            Paragraph(
                difficulty,
                normal_style,
            ),
        ],

        [
            Paragraph(
                "<b>Duration</b>",
                normal_style,
            ),
            Paragraph(
                f"{duration} minutes",
                normal_style,
            ),
        ],

        [
            Paragraph(
                "<b>Submitted</b>",
                normal_style,
            ),
            Paragraph(
                submitted,
                normal_style,
            ),
        ],
    ]

    details_table = Table(
        details_data,
        colWidths=[
            1.55 * inch,
            5.35 * inch,
        ],
        hAlign="CENTER",
    )

    details_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                LIGHT_BLUE,
            ),

            (
                "BACKGROUND",
                (1, 0),
                (1, -1),
                WHITE,
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (0, -1),
                DARK_BLUE,
            ),

            (
                "TEXTCOLOR",
                (1, 0),
                (1, -1),
                DARK_GRAY,
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.6,
                BORDER,
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                10,
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                10,
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),
        ])
    )

    elements.append(
        details_table
    )

    elements.append(
        Spacer(1, 18)
    )

    # ========================================================
    # PERFORMANCE SUMMARY
    # ========================================================

    elements.append(
        Paragraph(
            "PERFORMANCE SUMMARY",
            section_style,
        )
    )

    performance_data = [

        [
            Paragraph(
                "<b>SCORE</b>",
                center_style,
            ),

            Paragraph(
                "<b>PERCENTAGE</b>",
                center_style,
            ),

            Paragraph(
                "<b>STATUS</b>",
                center_style,
            ),
        ],

        [
            Paragraph(
                f"<b>{attempt.score}</b> / "
                f"{attempt.total_marks}",
                ParagraphStyle(
                    "ScoreValue",
                    parent=center_style,
                    fontName="Helvetica-Bold",
                    fontSize=17,
                    textColor=DARK_BLUE,
                ),
            ),

            Paragraph(
                f"<b>{attempt.percentage}%</b>",
                ParagraphStyle(
                    "PercentageValue",
                    parent=center_style,
                    fontName="Helvetica-Bold",
                    fontSize=17,
                    textColor=DARK_BLUE,
                ),
            ),

            Paragraph(
                f"<b>{status}</b>",
                ParagraphStyle(
                    "StatusValue",
                    parent=center_style,
                    fontName="Helvetica-Bold",
                    fontSize=17,
                    textColor=status_color,
                ),
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
            24,
            42,
        ],
        hAlign="CENTER",
    )

    performance_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                LIGHT_GRAY,
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.8,
                BORDER,
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER",
            ),
        ])
    )

    elements.append(
        performance_table
    )

    elements.append(
        Spacer(1, 12)
    )

    # ========================================================
    # DETAILED STATISTICS
    # ========================================================

    stats_data = [

        [
            Paragraph(
                "<b>Total</b>",
                center_style,
            ),

            Paragraph(
                "<b>Correct</b>",
                center_style,
            ),

            Paragraph(
                "<b>Wrong</b>",
                center_style,
            ),

            Paragraph(
                "<b>Unanswered</b>",
                center_style,
            ),

            Paragraph(
                "<b>Negative</b>",
                center_style,
            ),

            Paragraph(
                "<b>Time</b>",
                center_style,
            ),
        ],

        [
            Paragraph(
                str(total_questions),
                center_style,
            ),

            Paragraph(
                f'<font color="#198754">'
                f"<b>{correct}</b>"
                f"</font>",
                center_style,
            ),

            Paragraph(
                f'<font color="#DC3545">'
                f"<b>{wrong}</b>"
                f"</font>",
                center_style,
            ),

            Paragraph(
                f'<font color="#F59E0B">'
                f"<b>{unanswered}</b>"
                f"</font>",
                center_style,
            ),

            Paragraph(
                f'<font color="#DC3545">'
                f"<b>{negative_marks}</b>"
                f"</font>",
                center_style,
            ),

            Paragraph(
                f"<b>{time_taken} min</b>",
                center_style,
            ),
        ],
    ]

    stats_table = Table(
        stats_data,
        colWidths=[
            1.15 * inch,
            1.05 * inch,
            1.05 * inch,
            1.15 * inch,
            1.15 * inch,
            1.35 * inch,
        ],
    )

    stats_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                LIGHT_BLUE,
            ),

            (
                "BACKGROUND",
                (0, 1),
                (-1, 1),
                WHITE,
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.6,
                BORDER,
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6,
            ),
        ])
    )

    elements.append(
        stats_table
    )

    elements.append(
        Spacer(1, 18)
    )

    # ========================================================
    # RESULT MESSAGE
    # ========================================================

    message = (

        "Congratulations! You have successfully "
        "completed the examination."

        if attempt.is_passed

        else

        "Thank you for completing the examination."
    )

    message_table = Table(
        [[
            Paragraph(
                message,
                ParagraphStyle(
                    "ResultMessage",
                    parent=center_style,
                    fontName="Helvetica-Bold",
                    fontSize=10,
                    leading=14,
                    textColor=DARK_BLUE,
                ),
            )
        ]],
        colWidths=[
            doc.width
        ],
    )

    message_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                LIGHT_BLUE,
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.6,
                BORDER,
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8,
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8,
            ),
        ])
    )

    elements.append(
        message_table
    )

    # ========================================================
    # PAGE BREAK
    # ========================================================

    elements.append(
        PageBreak()
    )

    # ========================================================
    # QUESTION ANALYSIS
    # ========================================================

    elements.append(
        Paragraph(
            "QUESTION ANALYSIS",
            section_style,
        )
    )

    elements.append(
        Paragraph(
            "Detailed review of your submitted answers.",
            ParagraphStyle(
                "AnalysisSubtitle",
                parent=normal_style,
                textColor=GRAY,
                fontSize=8.5,
                spaceAfter=12,
            ),
        )
    )

    # ========================================================
    # QUESTIONS
    # ========================================================

    for index, answer in enumerate(
        answers,
        start=1,
    ):

        question = answer.question

        selected = answer.selected_option

        question_number = getattr(
            question,
            "question_number",
            index,
        )

        # ----------------------------------------------------
        # QUESTION TEXT
        # ----------------------------------------------------

        question_header = Paragraph(
            f"Question {question_number}",
            ParagraphStyle(
                "QuestionHeader",
                parent=section_style,
                fontSize=11,
                spaceAfter=4,
            ),
        )

        question_text = Paragraph(
            str(question.question_text),
            question_style,
        )

        # ----------------------------------------------------
        # YOUR ANSWER
        # ----------------------------------------------------

        if selected:

            selected_text = str(
                selected.option_text
            )

            if selected.is_correct:

                answer_color = "#198754"
                symbol = "✓"

            else:

                answer_color = "#DC3545"
                symbol = "✗"

            your_answer = Paragraph(
                f"<b>Your Answer:</b> "
                f'<font color="{answer_color}">'
                f"{selected_text} {symbol}"
                f"</font>",
                normal_style,
            )

        else:

            your_answer = Paragraph(
                "<b>Your Answer:</b> "
                '<font color="#6C757D">'
                "Not answered"
                "</font>",
                normal_style,
            )

        # ----------------------------------------------------
        # CORRECT ANSWER
        # ----------------------------------------------------

        correct_options = []

        for option in question.options.all():

            if option.is_correct:

                correct_options.append(
                    str(option.option_text)
                )

        correct_text = ", ".join(
            correct_options
        )

        correct_answer = Paragraph(
            f"<b>Correct Answer:</b> "
            f'<font color="#198754">'
            f"{correct_text}"
            f"</font>",
            normal_style,
        )

        # ----------------------------------------------------
        # MARKS
        # ----------------------------------------------------

        awarded = answer.marks_awarded

        max_marks = (
            attempt.exam.marks_per_question
        )

        if awarded < 0:

            marks_color = "#DC3545"

        else:

            marks_color = "#198754"

        marks_text = Paragraph(
            f"<b>Marks Awarded:</b> "
            f'<font color="{marks_color}">'
            f"<b>{awarded}</b>"
            f"</font>"
            f" / {max_marks}",
            normal_style,
        )

        # ----------------------------------------------------
        # EXPLANATION
        # ----------------------------------------------------

        question_elements = [

            question_header,

            question_text,

            Spacer(1, 6),

            your_answer,

            Spacer(1, 3),

            correct_answer,

            Spacer(1, 3),

            marks_text,
        ]

        if question.explanation:

            question_elements.extend([

                Spacer(1, 7),

                Table(
                    [[
                        Paragraph(
                            f"<b>Explanation:</b><br/>"
                            f"{str(question.explanation)}",
                            explanation_style,
                        )
                    ]],
                    colWidths=[
                        doc.width
                    ],
                    style=TableStyle([
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, -1),
                            LIGHT_BLUE,
                        ),
                        (
                            "BOX",
                            (0, 0),
                            (-1, -1),
                            0.6,
                            BORDER,
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            8,
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            8,
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            7,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            7,
                        ),
                    ]),
                ),
            ])

        question_elements.extend([

            Spacer(1, 12),

            HRFlowable(
                width="100%",
                thickness=0.5,
                color=BORDER,
                spaceBefore=2,
                spaceAfter=10,
            ),
        ])

        # Keep question header + content together where possible
        elements.append(
            KeepTogether(
                question_elements
            )
        )

    # ========================================================
    # SIGNATURE
    # ========================================================

    elements.append(
        Spacer(1, 20)
    )

    signature_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "sig-no-bg.png",
    )

    if os.path.exists(signature_path):

        try:

            signature = Image(
                signature_path,
                width=1.55 * inch,
                height=0.50 * inch,
            )

            signature_block = Table(
                [
                    [signature],
                    [
                        "____________________________"
                    ],
                    [
                        "Exam Administrator"
                    ],
                    [
                        "Authorized Signature • AI Exam Portal"
                    ],
                ],
                colWidths=[
                    2.2 * inch
                ],
                hAlign="RIGHT",
            )

            signature_block.setStyle(
                TableStyle([

                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER",
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),

                    (
                        "FONTNAME",
                        (0, 1),
                        (0, 1),
                        "Helvetica",
                    ),

                    (
                        "FONTNAME",
                        (0, 2),
                        (0, 2),
                        "Helvetica-Bold",
                    ),

                    (
                        "FONTNAME",
                        (0, 3),
                        (0, 3),
                        "Helvetica",
                    ),

                    (
                        "FONTSIZE",
                        (0, 1),
                        (0, 1),
                        8,
                    ),

                    (
                        "FONTSIZE",
                        (0, 2),
                        (0, 2),
                        9,
                    ),

                    (
                        "FONTSIZE",
                        (0, 3),
                        (0, 3),
                        7,
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 2),
                        (0, 2),
                        DARK_BLUE,
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 3),
                        (0, 3),
                        GRAY,
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        1,
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        1,
                    ),
                ])
            )

            elements.append(
                signature_block
            )

        except Exception:
            pass

    # ========================================================
    # RESULT ID / FINAL FOOTER
    # ========================================================

    elements.append(
        Spacer(1, 18)
    )

    elements.append(
        HRFlowable(
            width="100%",
            thickness=0.7,
            color=BORDER,
            spaceBefore=5,
            spaceAfter=8,
        )
    )

    if attempt.submitted_at:

        date_part = (
            attempt.submitted_at.strftime(
                "%Y%m%d"
            )
        )

    else:

        date_part = "NA"

    result_id = (
        f"RESULT-{date_part}-"
        f"{attempt.id:04d}"
    )

    footer_text = (
        f"<b>Result ID:</b> {result_id}<br/>"
        "This result report is digitally generated and "
        "verified by AI Exam Portal."
    )

    elements.append(
        Paragraph(
            footer_text,
            ParagraphStyle(
                "FinalFooter",
                parent=center_style,
                fontName="Helvetica",
                fontSize=7.5,
                leading=10,
                textColor=GRAY,
            ),
        )
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(
        elements,
        onFirstPage=draw_header_footer,
        onLaterPages=draw_header_footer,
    )