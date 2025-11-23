from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Complaint
from .forms import ComplaintForm, UserRegisterForm


# -------------------------------
#  USER REGISTER
# -------------------------------
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now login.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, "core/register.html", {"form": form})


# -------------------------------
#  USER LOGIN
# -------------------------------
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "core/login.html", {"form": form})


# -------------------------------
#  USER LOGOUT
# -------------------------------
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")


# -------------------------------
#  DASHBOARD (After Login)
# -------------------------------
@login_required
def dashboard(request):
    user = request.user

    # If admin/staff — can view all complaints
    if hasattr(user, "profile") and user.profile.role in ["staff", "admin"]:
        complaints = Complaint.objects.all().order_by("-created_at")
    else:
        # student can view only their own
        complaints = Complaint.objects.filter(user=user).order_by("-created_at")

    return render(request, "core/dashboard.html", {"complaints": complaints})


# -------------------------------
#  REPORT COMPLAINT (Only if logged in)
# -------------------------------
@login_required
def report_complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user  # attach logged-in user
            complaint.save()

            messages.success(request, "Complaint submitted successfully!")
            return redirect("complaint_list")
        else:
            messages.error(request, "Please fix the errors.")
    else:
        form = ComplaintForm()

    return render(request, "core/complaint_form.html", {"form": form})


# -------------------------------
#  LIST + SEARCH + FILTER COMPLAINTS
# -------------------------------
def complaint_list(request):
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()

    complaints = Complaint.objects.all().order_by("-created_at")

    # search logic
    if q:
        complaints = complaints.filter(
            models.Q(title__icontains=q)
            | models.Q(description__icontains=q)
            | models.Q(location__icontains=q)
        )

    # filter logic
    if category:
        complaints = complaints.filter(category=category)

    if status:
        complaints = complaints.filter(status=status)

    category_choices = Complaint._meta.get_field("category").choices
    status_choices = Complaint._meta.get_field("status").choices

    return render(
        request,
        "core/complaint_list.html",
        {
            "complaints": complaints,
            "q": q,
            "selected_category": category,
            "selected_status": status,
            "category_choices": category_choices,
            "status_choices": status_choices,
        },
    )
