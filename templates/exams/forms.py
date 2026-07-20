from django import forms
from .models import Exam


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            'title',
            'subject',
            'description',
            'difficulty',
            'duration_minutes'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }