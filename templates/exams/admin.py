from django.contrib import admin
from .models import Exam


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'difficulty', 'duration_minutes', 'created_by')
    search_fields = ('title', 'subject')
    list_filter = ('difficulty', 'subject')