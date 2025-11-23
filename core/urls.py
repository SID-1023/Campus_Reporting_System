from django.urls import path
from . import views

urlpatterns = [
    # Home → redirect to report (you can change later)
    path('', views.report_complaint, name='home'),

    # Complaint system
    path('report/', views.report_complaint, name='report_complaint'),
    path('complaints/', views.complaint_list, name='complaint_list'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboard (after login)
    path('dashboard/', views.dashboard, name='dashboard'),
]
