# exams/views.py
from io import BytesIO
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.urls import reverse_lazy

from django.views import View

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    TemplateView,
)

from django.utils import timezone

from django.db.models import (
    Avg,
    Max
)
from django.http import (
    JsonResponse,
    FileResponse
)
from .forms import ExamForm

from .models import (
    Exam,
    Question,
    Option,
    ExamAttempt,
    StudentAnswer,
    AIAnalysis
)
from .utils import analyze_performance
from .pdf_utils import build_result_pdf
from .services.ai_analyzer import generate_ai_feedback
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from .certificate_utils import build_certificate_pdf

# ==================================================
# Exam CRUD
# ==================================================

class ExamListView(ListView):

    model = Exam

    template_name = "exams/exam_list.html"

    context_object_name = "exams"

    paginate_by = 5


    def get_queryset(self):

        queryset = Exam.objects.all()


        q = self.request.GET.get("q")

        subject = self.request.GET.get("subject")

        difficulty = self.request.GET.get("difficulty")


        if q:
            queryset = queryset.filter(
                title__icontains=q
            )


        if subject:
            queryset = queryset.filter(
                subject__icontains=subject
            )


        if difficulty:
            queryset = queryset.filter(
                difficulty=difficulty
            )


        return queryset
class ExamDetailView(DetailView):

    model = Exam

    template_name = "exams/exam_detail.html"
class ExamCreateView(LoginRequiredMixin, CreateView):

    model = Exam

    form_class = ExamForm

    template_name = "exams/exam_form.html"

    success_url = reverse_lazy(
        "exam_list"
    )


    def form_valid(self,form):

        form.instance.created_by = self.request.user

        messages.success(
            self.request,
            "Exam created successfully!"
        )

        return super().form_valid(form)

class ExamUpdateView(LoginRequiredMixin, UpdateView):

    model = Exam

    form_class = ExamForm

    template_name = "exams/exam_form.html"

    success_url = reverse_lazy(
        "exam_list"
    )


    def form_valid(self,form):

        messages.success(
            self.request,
            "Exam updated successfully!"
        )

        return super().form_valid(form)




class ExamDeleteView(LoginRequiredMixin, DeleteView):

    model = Exam

    template_name = "exams/exam_confirm_delete.html"

    success_url = reverse_lazy(
        "exam_list"
    )


    def form_valid(self,form):

        messages.success(
            self.request,
            "Exam deleted successfully!"
        )

        return super().form_valid(form)



# ==================================================
# Dashboard
# ==================================================
class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        attempts = ExamAttempt.objects.filter(
            student=self.request.user,
            is_submitted=True
        ).select_related("exam")

        # -----------------------------
        # Overall Statistics
        # -----------------------------
        percentages = []

        for attempt in attempts:
            if attempt.total_marks > 0:
                percentages.append(
                    (attempt.score / attempt.total_marks) * 100
                )

        average_score = (
            round(sum(percentages) / len(percentages), 2)
            if percentages else 0
        )

        highest_score = (
            round(max(percentages), 2)
            if percentages else 0
        )

        passed_count = sum(
            1 for p in percentages if p >= 40
        )

        failed_count = len(percentages) - passed_count

        pass_percentage = (
            round((passed_count / len(percentages)) * 100, 2)
            if percentages else 0
        )

        # -----------------------------
        # Subject-wise Average (%)
        # -----------------------------
        subject_stats = []

        subjects = attempts.values_list(
            "exam__subject",
            flat=True
        ).distinct()

        for subject in subjects:

            subject_attempts = attempts.filter(
                exam__subject=subject
            )

            subject_percentages = []

            for attempt in subject_attempts:

                if attempt.total_marks > 0:
                    subject_percentages.append(
                        (attempt.score / attempt.total_marks) * 100
                    )

            avg_percentage = (
                round(
                    sum(subject_percentages) / len(subject_percentages),
                    2
                )
                if subject_percentages else 0
            )

            subject_stats.append({
                "exam__subject": subject,
                "avg_score": avg_percentage,
            })

        # -----------------------------
        # Monthly Attempts
        # -----------------------------
        monthly_attempts = (
            attempts
            .annotate(month=TruncMonth("submitted_at"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        # -----------------------------
        # Context
        # -----------------------------
        context.update({

            "total_exams": Exam.objects.count(),

            "total_attempts": attempts.count(),

            "average_score": average_score,

            "highest_score": highest_score,

            "pass_percentage": pass_percentage,

            "passed_count": passed_count,

            "failed_count": failed_count,

            "pass_count": passed_count,

            "fail_count": failed_count,

            "subject_stats": subject_stats,

            "monthly_attempts": monthly_attempts,

            "recent_attempts": attempts.order_by(
                "-submitted_at"
            )[:5],

        })

        return context
# ==================================================
# Exam Engine
# ==================================================
class StartExamView(LoginRequiredMixin, View):

    def get(self, request, pk):

        exam = get_object_or_404(
            Exam,
            pk=pk
        )


        submitted = ExamAttempt.objects.filter(

            student=request.user,

            exam=exam,

            is_submitted=True

        ).exists()



        if submitted:

            messages.warning(
                request,
                "You have already submitted this exam."
            )

            return redirect(
                "result_history"
            )



        attempt, created = ExamAttempt.objects.get_or_create(

            student=request.user,

            exam=exam,

            is_submitted=False

        )



        if created:

            messages.success(
                request,
                "Exam started successfully."
            )



        return redirect(
            "take_exam",
            attempt_id=attempt.id
        )

class TakeExamView(LoginRequiredMixin, View):
    template_name = "exams/take_exam.html"
    def get(self,request,attempt_id):

        attempt = get_object_or_404(

            ExamAttempt,

            id=attempt_id,

            student=request.user

        )


        if attempt.is_submitted:

            return redirect(
                "result_detail",
                pk=attempt.id
            )

        questions = (
            attempt.exam.questions
            .order_by("question_number")  # Keep questions in order
            .prefetch_related("options")
        )
        # Randomize only options
        for question in questions:
            question.random_options = question.options.order_by("?")

        existing_answers = {

            ans.question_id:
            ans.selected_option_id

            for ans in attempt.answers.all()

        }



        return render(

            request,

            self.template_name,

            {
                "attempt":attempt,
                "questions":questions,
                "existing_answers": existing_answers,
                "server_time": timezone.now(),
            }
        )

    def post(self,request,attempt_id):

        attempt = get_object_or_404(

            ExamAttempt,

            id=attempt_id,

            student=request.user

        )


        for question in attempt.exam.questions.all():

            option_id = request.POST.get(

                f"question_{question.id}"

            )


            if option_id:

                option = get_object_or_404(

                    Option,

                    id=option_id

                )


                StudentAnswer.objects.update_or_create(

                    attempt=attempt,

                    question=question,

                    defaults={

                        "selected_option":
                        option

                    }

                )
        messages.success(

            request,

            "Answers saved successfully."

        )


        return redirect(

            "take_exam",

            attempt_id=attempt.id

        )





# ==================================================
# Submit Exam + AI Generation
# ==================================================


class SubmitExamView(LoginRequiredMixin,View):


    def post(self,request,attempt_id):

        attempt = get_object_or_404(

            ExamAttempt,

            id=attempt_id,

            student=request.user

        )


        if attempt.is_submitted:

            return redirect(

                "result_detail",

                pk=attempt.id
            )
        total_marks = 0
        score = 0
        for question in attempt.exam.questions.all():
            
            total_marks += attempt.exam.marks_per_question
            
            option_id = request.POST.get(

                f"question_{question.id}"

            )


            if option_id:
                option = get_object_or_404(
                    Option,
                    id=option_id
                )
                answer, created = (
                    StudentAnswer.objects
                    .update_or_create(
                        attempt=attempt,
                        question=question,
                        defaults={
                            "selected_option":
                            option
                        }
                    )
                )

                if option.is_correct:
                    answer.marks_awarded = attempt.exam.marks_per_question
                    score += attempt.exam.marks_per_question
                else:

                    if attempt.exam.negative_marking:
                        negative_marks = attempt.exam.negative_marks
                        answer.marks_awarded = -negative_marks
                        score -= negative_marks

                    else:
                        answer.marks_awarded = 0

                answer.save()

        attempt.score = score

        attempt.total_marks = total_marks

        attempt.is_submitted = True

        attempt.submitted_at = timezone.now()

        attempt.save()

        # ================================
        # Generate AI Feedback
        # ================================


        feedback = generate_ai_feedback(

            attempt

        )



        AIAnalysis.objects.update_or_create(

            attempt=attempt,

            defaults={

                "strengths":
                feedback["strengths"],


                "weaknesses":
                feedback["weaknesses"],


                "recommendations":
                feedback["recommendations"],


                "overall_feedback":
                feedback["overall_feedback"]

            }

        )



        messages.success(

            request,

            "Exam submitted successfully."

        )


        return redirect(

            "ai_feedback",

            pk=attempt.id

        )
# ==================================================
# Results
# ==================================================


class ResultDetailView(LoginRequiredMixin,View):

    template_name="exams/result_detail.html"



    def get(self, request, pk):

        attempt = get_object_or_404(
            ExamAttempt,
            id=pk,
            student=request.user
        )

        answers = attempt.answers.select_related(
            "question",
            "selected_option"
        )

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
                    negative_marks += abs(answer.marks_awarded)

        total_questions = attempt.exam.questions.count()

        unanswered = total_questions - (correct + wrong)

        if attempt.submitted_at:
            time_taken = round((
                attempt.submitted_at - attempt.started_at
            ).total_seconds() / 60,2)
        else:
            time_taken = 0

        analysis = analyze_performance(attempt)

        return render(
            request,
            self.template_name,
            {
                "attempt": attempt,
                "answers": answers,
                "analysis": analysis,
                "correct": correct,
                "wrong": wrong,
                "unanswered": unanswered,
                "negative_marks": negative_marks,
                "time_taken": time_taken,
            },
        )
class ResultListView(LoginRequiredMixin,View):

    template_name="exams/result_list.html"



    def get(self,request):


        attempts = ExamAttempt.objects.filter(

            student=request.user,

            is_submitted=True

        ).select_related(
            "exam"
        )


        return render(

            request,

            self.template_name,

            {

                "attempts":attempts

            }

        )

# ==================================================
# Performance Analytics
# ==================================================
class PerformanceAnalyticsView(
    LoginRequiredMixin,
    TemplateView
):

    template_name="exams/analytics.html"



    def get_context_data(self,**kwargs):

        context = super().get_context_data(**kwargs)

        attempts = ExamAttempt.objects.filter(
            student=self.request.user,
            is_submitted=True
        )

        subject_stats = (
            attempts.values("exam__subject")
            .annotate(avg_score=Avg("score"))
        )

        subject_labels = []
        subject_scores = []

        for item in subject_stats:
            subject_labels.append(item["exam__subject"])
            subject_scores.append(float(item["avg_score"]))

        context["subject_labels"] = subject_labels
        context["subject_scores"] = subject_scores

        total = attempts.count()
        average = (

            attempts.aggregate(
                Avg("score")
            )["score__avg"]
            or 0
        )

        highest = (

            attempts.aggregate(
                Max("score")
            )["score__max"]
            or 0
        )
        passed = sum(
            1 for a in attempts
            if a.is_passed
        )
        pass_percentage = (

            passed/total*100

            if total else 0
        )
        passed_count = 0
        failed_count = 0

        for attempt in attempts:
            if attempt.is_passed:
                passed_count += 1
            else:
                failed_count += 1
        
        context.update({
            "total_exams": total,
            "average_score": round(average, 2),
            "highest_score": highest,
            "pass_percentage": round(pass_percentage, 2),
            "passed_count": passed_count,
            "failed_count": failed_count,
            "attempts": attempts,
        })
        return context
# ==================================================
# PDF Result
# ==================================================
class ResultPDFView(LoginRequiredMixin,View):
    def get(self,request,pk):

        attempt = get_object_or_404(
            ExamAttempt,
            id=pk,
            student=request.user
        )
        buffer = BytesIO()

        build_result_pdf(
            buffer,
            attempt
        )
        buffer.seek(0)

        return FileResponse(

            buffer,

            as_attachment=True,

            filename=f"result_{attempt.id}.pdf"
        )

# ==================================================
# AI Feedback Page
# ==================================================
class AIFeedbackView(LoginRequiredMixin, DetailView):
    model = ExamAttempt
    template_name = "exams/ai_feedback.html"
    context_object_name = "attempt"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempt = self.object

        if attempt.percentage >= 80:
            context["ai_insight"] = (
                "Excellent work! You have a strong understanding of the subject."
            )
        elif attempt.percentage >= 40:
            context["ai_insight"] = (
                "Good attempt. Focus on revising incorrect answers and practicing more problems."
            )
        else:
            context["ai_insight"] = (
                "You need more practice. Revise the fundamentals and attempt the exam again."
            )
        return context
# ==================================================
# AI Manual Generate Endpoint
# ==================================================


@login_required
def generate_ai_analysis(request,attempt_id):


    attempt = get_object_or_404(

        ExamAttempt,

        id=attempt_id,

        student=request.user

    )


    feedback = generate_ai_feedback(

        attempt

    )


    AIAnalysis.objects.update_or_create(

        attempt=attempt,

        defaults={

            "strengths":
            feedback["strengths"],


            "weaknesses":
            feedback["weaknesses"],


            "recommendations":
            feedback["recommendations"],


            "overall_feedback":
            feedback["overall_feedback"]

        }

    )


    return redirect(

        "ai_feedback",

        pk=attempt.id

    )

# ==================================================
# API
# ==================================================


@login_required
def exam_stats_api(request,pk):
    exam = get_object_or_404(
        Exam,
        pk=pk
    )
    attempts = ExamAttempt.objects.filter(
        exam=exam,
        is_submitted=True
    )
    total = attempts.count()
    data={
        "exam":
        exam.title,
        "subject":
        exam.subject,
        "attempts":
        total
    }
    return JsonResponse(data)
@login_required
def download_result_pdf(request, pk):
    result = get_object_or_404(
        ExamAttempt,
        pk=pk,
        student=request.user
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="result_{result.id}.pdf"'
    )

    p = canvas.Canvas(response)

    # Title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(180, 800, "AI Exam Portal")

    # Student details
    p.setFont("Helvetica", 14)
    p.drawString(50, 750, f"Student: {result.student.username}")
    p.drawString(50, 720, f"Exam: {result.exam.title}")
    p.drawString(50, 690, f"Subject: {result.exam.subject}")

    # Score
    p.drawString(
        50,
        650,
        f"Score: {result.score}/{result.total_marks}"
    )

    p.drawString(
        50,
        620,
        f"Percentage: {result.percentage}%"
    )

    # Status
    status = "PASS" if result.is_passed else "FAIL"
    p.drawString(50, 590, f"Status: {status}")

    # Submission time
    if result.submitted_at:
        p.drawString(
            50,
            550,
            f"Submitted: {result.submitted_at.strftime('%d-%m-%Y %H:%M')}"
        )

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 500, "Generated by AI Exam Portal")

    p.showPage()
    p.save()

    return response


class ExamInstructionsView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = "exams/instructions.html"
    context_object_name = "exam"


class DownloadCertificateView(LoginRequiredMixin, View):

    def get(self, request, pk):

        attempt = get_object_or_404(
            ExamAttempt,
            id=pk,
            student=request.user
        )

        # Allow only passed students
        if not attempt.is_passed:

            messages.error(
                request,
                "You must pass the exam to download the certificate."
            )

            return redirect(
                "result_detail",
                pk=attempt.id
            )

        buffer = BytesIO()

        build_certificate_pdf(
            buffer,
            attempt
        )

        buffer.seek(0)

        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f"certificate_{attempt.id}.pdf"
        )