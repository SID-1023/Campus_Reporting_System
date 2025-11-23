from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Complaint, Profile

# --------------------------
# Complaint Submission Form
# --------------------------

class ComplaintForm(forms.ModelForm):
    # Optional: Allow anonymous submissions
    anonymous = forms.BooleanField(
        required=False,
        label="Submit anonymously",
    )

    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category', 'location', 'image', 'anonymous']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complaint title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the issue...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location (Building, Room No. etc.)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

# --------------------------
# User Registration Form
# --------------------------

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # Dropdown for user role
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        initial='student',
        label="Select Role",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # Ensure Profile exists, create if not
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data.get('role')
            profile.save()

        return user
