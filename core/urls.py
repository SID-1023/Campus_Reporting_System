from django.urls import path
from . import views

urlpatterns = [
    # Home → redirect to report
    path('', views.report_complaint, name='home'),

    # Complaint system
    path('report/', views.report_complaint, name='report_complaint'),
    path('complaints/', views.complaint_list, name='complaint_list'),

    # Pending complaints (staff/admin)
    path('complaints/pending/', views.pending_complaints, name='pending_complaints'),

    # Update complaint status (POST only)
    path('complaint/<int:complaint_id>/update/<str:new_status>/', views.update_status, name='update_status'),

    # Complaint detail view
    path('complaint/<int:complaint_id>/detail/', views.complaint_detail, name='complaint_detail'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
