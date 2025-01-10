from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, School, Teacher, Student
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()

class ProfileUpdateForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = forms.CharField(validators=[phone_regex], max_length=17, required=False)

    class Meta:
        model = User
        fields = ['email', 'phone_number']

# School Registration Form
class SchoolRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'name', 'address']

# Add Teacher Form
class AddTeacherForm(forms.ModelForm):
    email = forms.EmailField(label="Teacher Email", required=True)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        initial="12345678",  # Default password
        help_text="Default password is '12345678'. Teachers can change it after logging in."
    )

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'password']

# Add Student Form
class AddStudentForm(forms.ModelForm):
    email = forms.EmailField(label="Student Email", required=True)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        initial="12345678",  # Default password
        help_text="Default password is '12345678'. Student can change it after logging in."
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'password']

class StudentPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User

# Password Change Form for Teachers
class TeacherPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User