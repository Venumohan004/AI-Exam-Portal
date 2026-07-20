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
            'duration_minutes',
        ]

        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
        }