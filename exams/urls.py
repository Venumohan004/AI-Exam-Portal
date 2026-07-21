from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('<int:pk>/', views.exam_detail, name='exam_detail'),

    path('<int:pk>/start/', views.StartExamView.as_view(), name='start_exam'),
    path('attempt/<int:attempt_id>/', views.TakeExamView.as_view(), name='take_exam'),
    path('attempt/<int:attempt_id>/submit/', views.SubmitExamView.as_view(), name='submit_exam'),

    path('results/', views.ResultListView.as_view(), name='result_list'),
    path('results/<int:pk>/', views.ResultDetailView.as_view(), name='result_detail'),
]