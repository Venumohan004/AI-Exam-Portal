from django import forms
from django.forms import inlineformset_factory
from .models import Exam, Question, Option


# Existing Exam form (required by views.py)
class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam

        fields = [
            'title',
            'subject',
            'description',
            'duration_minutes',
            'marks_per_question',
            'negative_marking',
            'negative_marks',
            'difficulty'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),

            'marks_per_question': forms.NumberInput(
                attrs={
                    'step': '0.25',
                    'min': '0'
                }
            ),

            'negative_marks': forms.NumberInput(
                attrs={
                    'step': '0.25',
                    'min': '0'
                }
            ),
        }

# Question form
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'marks', 'explanation']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 3}),
            'explanation': forms.Textarea(attrs={'rows': 3}),
        }


# Option form
class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['option_text', 'is_correct']


# Inline formset for options
OptionFormSet = inlineformset_factory(
    Question,
    Option,
    form=OptionForm,
    extra=4,
    min_num=2,
    validate_min=True,
    can_delete=False
)