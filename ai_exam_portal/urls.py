"""
URL configuration for ai_exam_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from exams.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),

    # Accounts app
    path('accounts/', include('accounts.urls')),

    # Login
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    # Logout  ✅ IMPORTANT
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # Exams
    path('exams/', include('exams.urls')),
]