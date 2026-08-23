# Register your models here.
from django.contrib import admin
from .models import (
    Exam,
    Question,
    Option,
    ExamAttempt,
    StudentAnswer
)


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4
    min_num = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'exam', 'question_text' ]
    search_fields = ['question_text', 'exam__title']
    inlines = [OptionInline]


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'subject',
        'difficulty',
        'duration_minutes',
        'question_count',
        'created_at'
    ]
    list_filter = ['subject', 'difficulty']
    search_fields = ['title', 'subject']


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'exam',
        'score',
        'total_marks',
        'is_submitted',
        'started_at',
        'submitted_at'
    ]
    list_filter = ['is_submitted', 'exam__subject']
    search_fields = ['student__username', 'exam__title']
    readonly_fields = ['score', 'total_marks', 'submitted_at']


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selected_option', 'marks_awarded']
    search_fields = ['attempt__student__username', 'question__question_text']
