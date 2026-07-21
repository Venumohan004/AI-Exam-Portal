from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ExamForm
from .models import Exam

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.utils import timezone

from .models import (
    Exam,
    Question,
    Option,
    ExamAttempt,
    StudentAnswer,
)
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ExamForm


class ExamListView(ListView):
    model = Exam
    template_name = 'exams/exam_list.html'
    context_object_name = 'exams'
    paginate_by = 5

    def get_queryset(self):
        queryset = Exam.objects.all()

        q = self.request.GET.get('q')
        subject = self.request.GET.get('subject')
        difficulty = self.request.GET.get('difficulty')

        if q:
            queryset = queryset.filter(title__icontains=q)

        if subject:
            queryset = queryset.filter(subject__icontains=subject)

        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        return queryset


class ExamDetailView(DetailView):
    model = Exam
    template_name = 'exams/exam_detail.html'


class ExamCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/exam_form.html'
    success_url = reverse_lazy('exam_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Exam created successfully!')
        return super().form_valid(form)


class ExamUpdateView(LoginRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/exam_form.html'
    success_url = reverse_lazy('exam_list')

    def form_valid(self, form):
        messages.success(self.request, 'Exam updated successfully!')
        return super().form_valid(form)


class ExamDeleteView(LoginRequiredMixin, DeleteView):
    model = Exam
    template_name = 'exams/exam_confirm_delete.html'
    success_url = reverse_lazy('exam_list')

    def form_valid(self, form):
        messages.success(self.request, 'Exam deleted successfully!')
        return super().form_valid(form)


def dashboard_view(request):
    total_exams = Exam.objects.count()
    total_subjects = Exam.objects.values('subject').distinct().count()
    total_easy = Exam.objects.filter(difficulty='Easy').count()
    total_hard = Exam.objects.filter(difficulty='Hard').count()
    recent_exams = Exam.objects.all()[:5]

    context = {
        'total_exams': total_exams,
        'total_subjects': total_subjects,
        'total_easy': total_easy,
        'total_hard': total_hard,
        'recent_exams': recent_exams,
    }

    return render(request, 'dashboard.html', context)

class StartExamView(LoginRequiredMixin, View):
    def get(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)

        submitted = ExamAttempt.objects.filter(
            student=request.user,
            exam=exam,
            is_submitted=True
        ).exists()

        if submitted:
            messages.warning(request, "You have already submitted this exam.")
            return redirect('result_list')

        attempt, created = ExamAttempt.objects.get_or_create(
            student=request.user,
            exam=exam,
            is_submitted=False
        )

        if created:
            messages.success(request, "Exam started successfully.")

        return redirect('take_exam', attempt_id=attempt.id)


class TakeExamView(LoginRequiredMixin, View):
    template_name = 'exams/take_exam.html'

    def get(self, request, attempt_id):
        attempt = get_object_or_404(
            ExamAttempt,
            id=attempt_id,
            student=request.user
        )

        if attempt.is_submitted:
            return redirect('result_detail', pk=attempt.id)

        questions = attempt.exam.questions.prefetch_related('options')

        existing_answers = {
            ans.question_id: ans.selected_option_id
            for ans in attempt.answers.all()
        }

        return render(request, self.template_name, {
            'attempt': attempt,
            'questions': questions,
            'existing_answers': existing_answers,
        })

    def post(self, request, attempt_id):
        attempt = get_object_or_404(
            ExamAttempt,
            id=attempt_id,
            student=request.user
        )

        questions = attempt.exam.questions.all()

        for question in questions:
            option_id = request.POST.get(f'question_{question.id}')

            if option_id:
                option = Option.objects.get(id=option_id)

                StudentAnswer.objects.update_or_create(
                    attempt=attempt,
                    question=question,
                    defaults={'selected_option': option}
                )

        messages.success(request, "Answers saved successfully.")
        return redirect('take_exam', attempt_id=attempt.id)


class SubmitExamView(LoginRequiredMixin, View):
    def post(self, request, attempt_id):
        attempt = get_object_or_404(
            ExamAttempt,
            id=attempt_id,
            student=request.user
        )

        if attempt.is_submitted:
            messages.warning(request, "Exam already submitted.")
            return redirect('result_detail', pk=attempt.id)

        # STEP 1: Save submitted answers
        for question in attempt.exam.questions.all():
            option_id = request.POST.get(f'question_{question.id}')

            if option_id:
                option = get_object_or_404(Option, id=option_id)

                StudentAnswer.objects.update_or_create(
                    attempt=attempt,
                    question=question,
                    defaults={'selected_option': option}
                )

        # STEP 2: Calculate score
        total_marks = 0
        score = 0

        for question in attempt.exam.questions.all():
            total_marks += question.marks

            answer = StudentAnswer.objects.filter(
                attempt=attempt,
                question=question
            ).first()

            if answer and answer.selected_option:
                if answer.selected_option.is_correct:
                    answer.marks_awarded = question.marks
                    score += question.marks
                else:
                    answer.marks_awarded = 0

                answer.save()

        # STEP 3: Update attempt
        attempt.score = score
        attempt.total_marks = total_marks
        attempt.is_submitted = True
        attempt.submitted_at = timezone.now()
        attempt.save()

        messages.success(request, "Exam submitted successfully.")
        return redirect('result_detail', pk=attempt.id)


class ResultDetailView(LoginRequiredMixin, View):
    template_name = 'exams/result_detail.html'

    def get(self, request, pk):
        attempt = get_object_or_404(
            ExamAttempt,
            id=pk,
            student=request.user
        )

        answers = attempt.answers.select_related(
            'question',
            'selected_option'
        )

        return render(request, self.template_name, {
            'attempt': attempt,
            'answers': answers,
        })


class ResultListView(LoginRequiredMixin, View):
    template_name = 'exams/result_list.html'

    def get(self, request):
        attempts = ExamAttempt.objects.filter(
            student=request.user,
            is_submitted=True
        ).select_related('exam')

        search = request.GET.get('q')

        if search:
            attempts = attempts.filter(exam__title__icontains=search)

        return render(request, self.template_name, {
            'attempts': attempts,
            'search': search,
        })
    
@login_required
def exam_list(request):
    exams = Exam.objects.all()

    query = request.GET.get('q')
    subject = request.GET.get('subject')
    difficulty = request.GET.get('difficulty')

    if query:
        exams = exams.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query)
        )

    if subject:
        exams = exams.filter(subject__icontains=subject)

    if difficulty:
        exams = exams.filter(difficulty=difficulty)

    paginator = Paginator(exams, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'exams/exam_list.html', {
        'page_obj': page_obj,
        'query': query,
        'subject': subject,
        'difficulty': difficulty,
    })


@login_required
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    return render(request, 'exams/exam_detail.html', {
        'exam': exam
    })