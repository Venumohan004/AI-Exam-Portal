from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q


# =========================
# Exam Model
# =========================
class Exam(models.Model):

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    duration_minutes = models.PositiveIntegerField(default=30)

    negative_marking = models.BooleanField(
        default=False,
        help_text="Enable negative marking for incorrect answers."
    )

    negative_marks = models.FloatField(
        default=0.25,
        help_text="Marks deducted for each incorrect answer."
    )

    marks_per_question = models.FloatField(
        default=1,
        help_text="Marks awarded for each correct answer."
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def question_count(self):
        return self.questions.count()



# =========================
# Question Model
# =========================
class Question(models.Model):

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    question_number = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    question_text = models.TextField()

    marks = models.FloatField(
        default=1
    )

    explanation = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        ordering = ['question_number']

    def __str__(self):
        return f"{self.exam.title} - Question {self.question_number}"

    def save(self, *args, **kwargs):

        if not self.question_number:

            last_question = (
                Question.objects.filter(exam=self.exam)
                .aggregate(models.Max("question_number"))["question_number__max"] or 0
            )

            self.question_number = last_question + 1

        super().save(*args, **kwargs)

# =========================
# Option Model
# =========================
class Option(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options"
    )

    option_text = models.CharField(
        max_length=255
    )

    is_correct = models.BooleanField(
        default=False
    )


    class Meta:
        ordering = ['id']


    def __str__(self):
        return self.option_text




# =========================
# Exam Attempt / Result Model
# =========================
class ExamAttempt(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="exam_attempts"
    )


    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="attempts"
    )


    started_at = models.DateTimeField(
        auto_now_add=True
    )


    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )
    score = models.FloatField(
        default=0
    )

    total_marks = models.FloatField(default=0)

    is_submitted = models.BooleanField(
        default=False
    )



    class Meta:

        ordering = ['-started_at']


        constraints = [

            models.UniqueConstraint(
                fields=[
                    'student',
                    'exam'
                ],

                condition=Q(
                    is_submitted=True
                ),

                name="unique_submitted_attempt"
            )

        ]



    def __str__(self):

        return f"{self.student.username} - {self.exam.title}"

    # Percentage
    @property
    def percentage(self):

        if self.total_marks == 0:
            return 0


        return round(
            (self.score / self.total_marks) * 100,
            2
        )
    # Pass / Fail
    @property
    def is_passed(self):

        return self.percentage >= 40

    # Result Status
    @property
    def result_status(self):

        return "PASS" if self.is_passed else "FAIL"

# =========================
# Student Answer Model
# =========================
class StudentAnswer(models.Model):

    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name="answers"
    )


    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )


    selected_option = models.ForeignKey(
        Option,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    marks_awarded = models.FloatField(
        default=0
    )



    class Meta:

        unique_together = [
            'attempt',
            'question'
        ]

        ordering = [
            'question__id'
        ]



    def __str__(self):

        return (
            f"{self.attempt.student.username} "
            f"- Question {self.question.id}"
        )

# =========================
# AI Performance Analysis
# =========================

class AIAnalysis(models.Model):

    attempt = models.OneToOneField(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name="ai_analysis"
    )

    strengths = models.TextField()

    weaknesses = models.TextField()

    recommendations = models.TextField()

    overall_feedback = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"AI Report - {self.attempt.student.username}"