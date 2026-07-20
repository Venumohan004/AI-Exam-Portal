from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
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