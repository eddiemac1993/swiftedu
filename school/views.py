from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import SchoolRegistrationForm, AddTeacherForm, AddStudentForm, TeacherPasswordChangeForm
from .models import User, School, Teacher, Student
import random
import string

# School Registration View
def school_register(request):
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'school'
            user.save()

            # Create School Profile
            school = School.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address']
            )

            login(request, user)
            return redirect('school_dashboard')
    else:
        form = SchoolRegistrationForm()
    return render(request, 'school_register.html', {'form': form})

# School Dashboard View
@login_required
def school_dashboard(request):
    if request.user.user_type != 'school':
        return redirect('login')

    school = request.user.school
    teachers = Teacher.objects.filter(school=school)
    students = Student.objects.filter(school=school)

    return render(request, 'school_dashboard.html', {
        'school': school,
        'teachers': teachers,
        'students': students,
    })

@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # 'username' is the email field
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user type
                if user.user_type == 'school':
                    return redirect('school_dashboard')
                elif user.user_type == 'teacher':
                    return redirect('teacher_dashboard')
                elif user.user_type == 'student':
                    return redirect('student_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Add Teacher View
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import AddTeacherForm
from .models import Teacher

User = get_user_model()

@login_required
def add_teacher(request):
    if request.user.user_type != 'school':
        return redirect('login')

    if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            # Create User for Teacher
            teacher_user = User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                user_type='teacher'
            )

            # Create Teacher Profile
            teacher = Teacher.objects.create(
                user=teacher_user,
                school=request.user.school,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            # TODO: Send email to teacher with their credentials
            print(f"Teacher created with email: {teacher_user.email} and password: {form.cleaned_data['password']}")

            return redirect('school_dashboard')
    else:
        form = AddTeacherForm()
    return render(request, 'add_teacher.html', {'form': form})

# Add Student View
@login_required
def add_student(request):
    if request.user.user_type != 'school':
        return redirect('login')

    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            # Create User for Teacher
            student_user = User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                user_type='student'
            )

            # Create Teacher Profile
            student = Student.objects.create(
                user=student_user,
                school=request.user.school,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            # TODO: Send email to teacher with their credentials
            print(f"Student created with email: {student_user.email} and password: {form.cleaned_data['password']}")

            return redirect('school_dashboard')
    else:
        form = AddTeacherForm()
    return render(request, 'add_student.html', {'form': form})

# Teacher Password Change View
@login_required
def teacher_change_password(request):
    if request.user.user_type != 'teacher':
        return redirect('login')

    if request.method == 'POST':
        form = TeacherPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherPasswordChangeForm(request.user)
    return render(request, 'teacher_change_password.html', {'form': form})

@login_required
def student_change_password(request):
    if request.user.user_type != 'student':
        return redirect('login')

    if request.method == 'POST':
        form = StudentPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = StudentPasswordChangeForm(request.user)
    return render(request, 'student_change_password.html', {'form': form})