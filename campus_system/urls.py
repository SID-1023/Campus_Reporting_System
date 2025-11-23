from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Complaint reporting
    path('report/', views.report_complaint, name='report_complaint'),

    # Complaint list / search / filter
    path('complaints/', views.complaint_list, name='complaint_list'),

    # Include all other URLs from core app if any
    path('', include('core.urls')),
]
