from django.urls import path
from . import views
from .views import (
    ExamListView,
    ExamDetailView,
    ExamCreateView,
    ExamUpdateView,
    ExamDeleteView,
    StartExamView,
    TakeExamView,
    SubmitExamView,
    ResultDetailView,
    ResultListView,
    ResultPDFView,
    PerformanceAnalyticsView,
    exam_stats_api,
    AIFeedbackView,
    generate_ai_analysis,
    download_result_pdf,
    DownloadCertificateView
)


urlpatterns = [

    # ==========================
    # Exam CRUD
    # ==========================

    path(
        '',
        ExamListView.as_view(),
        name='exam_list'
    ),

    path(
        '<int:pk>/',
        ExamDetailView.as_view(),
        name='exam_detail'
    ),

    path(
        'create/',
        ExamCreateView.as_view(),
        name='exam_create'
    ),

    path(
        '<int:pk>/edit/',
        ExamUpdateView.as_view(),
        name='exam_update'
    ),

    path(
        '<int:pk>/delete/',
        ExamDeleteView.as_view(),
        name='exam_delete'
    ),
    
    path(
        "exam/<int:pk>/instructions/",
        views.ExamInstructionsView.as_view(),
        name="exam_instructions",
    ),

    # ==========================
    # Exam Engine
    # ==========================

    path(
        '<int:pk>/start/',
        StartExamView.as_view(),
        name='start_exam'
    ),

    path(
        'attempt/<int:attempt_id>/',
        TakeExamView.as_view(),
        name='take_exam'
    ),

    path(
        'attempt/<int:attempt_id>/submit/',
        SubmitExamView.as_view(),
        name='submit_exam'
    ),

    # ==========================
    # Results
    # ==========================

    path(
        'results/',
        ResultListView.as_view(),
        name='result_history'
    ),

    path(
        'results/<int:pk>/',
        ResultDetailView.as_view(),
        name='result_detail'
    ),

    path(
        'analytics/',
        PerformanceAnalyticsView.as_view(),
        name='performance_analytics'
    ),
    path(
        "result/<int:pk>/download/",
        download_result_pdf,
        name="download_result_pdf",
    ),
    path(
        "certificate/<int:pk>/",
        DownloadCertificateView.as_view(),
        name="download_certificate",
    ),
    # ==========================
    # AI Performance Analysis
    # ==========================

    path(
        'ai-analysis/<int:attempt_id>/',
        generate_ai_analysis,
        name='generate-ai-analysis'
    ),

    path(
        "ai-feedback/<int:pk>/",
        AIFeedbackView.as_view(),
        name="ai_feedback"
    ),

    # ==========================
    # API
    # ==========================

    path(
        'api/exams/<int:pk>/stats/',
        exam_stats_api,
        name='exam_stats_api'
    ),

]