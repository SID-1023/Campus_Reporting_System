from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import models

from .forms import ComplaintForm, UserRegisterForm
from .models import Complaint, Profile


# -------------------------------
#  USER REGISTER
# -------------------------------
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-create Profile if not exists
            Profile.objects.get_or_create(
                user=user, defaults={'role': form.cleaned_data.get('role')}
            )
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
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")


# -------------------------------
#  DASHBOARD
# -------------------------------
@login_required
def dashboard(request):
    user = request.user
    if hasattr(user, "profile") and user.profile.role in ["staff", "admin"]:
        complaints = Complaint.objects.all().order_by("-created_at")
    else:
        complaints = Complaint.objects.filter(user=user).order_by("-created_at")
    return render(request, "core/dashboard.html", {"complaints": complaints})


# -------------------------------
#  REPORT COMPLAINT
# -------------------------------
@login_required
def report_complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, "Complaint submitted successfully!")
            return redirect("complaint_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ComplaintForm()
    return render(request, "core/complaint_form.html", {"form": form})


# -------------------------------
#  LIST + SEARCH + FILTER COMPLAINTS
# -------------------------------
@login_required
def complaint_list(request):
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()

    complaints = Complaint.objects.all().order_by("-created_at")

    # Search logic
    if q:
        complaints = complaints.filter(
            models.Q(title__icontains=q)
            | models.Q(description__icontains=q)
            | models.Q(location__icontains=q)
        )

    # Filter by category
    if category:
        complaints = complaints.filter(category=category)

    # Filter by status
    if status:
        complaints = complaints.filter(status=status)

    category_choices = Complaint._meta.get_field("category").choices
    status_choices = Complaint._meta.get_field("status").choices

    context = {
        "complaints": complaints,
        "q": q,
        "selected_category": category,
        "selected_status": status,
        "category_choices": category_choices,
        "status_choices": status_choices,
    }
    return render(request, "core/complaint_list.html", context)


# -------------------------------
#  PENDING COMPLAINTS
# -------------------------------
@login_required
def pending_complaints(request):
    user = request.user
    if hasattr(user, "profile") and user.profile.role in ["staff", "admin"]:
        complaints = Complaint.objects.filter(status="pending").order_by("-created_at")
    else:
        messages.error(request, "You are not authorized to view pending complaints.")
        return redirect("dashboard")
    return render(request, "core/pending_complaints.html", {"complaints": complaints})


# -------------------------------
#  UPDATE COMPLAINT STATUS
# -------------------------------
@login_required
def update_status(request, complaint_id, new_status):
    if request.method == "POST":
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.status = new_status
        complaint.save()
        messages.success(
            request,
            f"Complaint '{complaint.title}' status updated to {new_status.replace('_',' ').title()}."
        )
    return redirect("pending_complaints")


# -------------------------------
#  VIEW COMPLAINT DETAIL
# -------------------------------
@login_required
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    return render(request, "core/complaint_detail.html", {"complaint": complaint})
