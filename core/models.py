from django.db import models
from django.contrib.auth.models import User

# ---------------------------------------------------------
# Choices for complaint category and status
# ---------------------------------------------------------
CATEGORY_CHOICES = [
    ('Infrastructure', 'Infrastructure'),
    ('Cleanliness', 'Cleanliness'),
    ('Technical', 'Technical'),
    ('Safety & Security', 'Safety & Security'),
    ('Administrative', 'Administrative'),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Resolved', 'Resolved'),
    ('Reopened', 'Reopened'),
]

# ---------------------------------------------------------
# Complaint Model
# ---------------------------------------------------------
class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.status}"


# ---------------------------------------------------------
# Profile Model (Extends User with Role)
# ---------------------------------------------------------
class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} ({self.role})"
