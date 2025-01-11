from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from .forms import SchoolRegistrationForm, AddTeacherForm, AddStudentForm, TeacherPasswordChangeForm, StudentPasswordChangeForm
from .models import User, School, Teacher, Student
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.contrib import messages
from .forms import ProfileUpdateForm

def send_welcome_email(email):
    subject = 'Welcome to Our Platform'
    message = 'Thank you for joining us!'
    from_email = 'edwardmanjolo9@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {
        'form': form,
    }
    return render(request, 'profile.html', context)

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id, school=request.user.school)
    student.user.delete()  # Delete the associated user
    return redirect('manage_students')

@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id, school=request.user.school)
    if request.method == 'POST':
        form = AddStudentForm(request.POST, instance=student.user)
        if form.is_valid():
            form.save()
            return redirect('manage_students')
    else:
        form = AddStudentForm(instance=student.user)
    return render(request, 'edit_student.html', {'form': form})

@login_required
def manage_students(request):
    # Ensure only schools can access this page
    if request.user.user_type != 'school':
        return redirect('login')

    # Fetch all students associated with the logged-in school
    school = request.user.school
    students = Student.objects.filter(school=school)

    return render(request, 'manage_students.html', {'students': students})

@login_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id, school=request.user.school)
    teacher.user.delete()  # Delete the associated user
    return redirect('manage_teachers')

@login_required
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id, school=request.user.school)
    if request.method == 'POST':
        form = AddTeacherForm(request.POST, instance=teacher.user)
        if form.is_valid():
            form.save()
            return redirect('manage_teachers')
    else:
        form = AddTeacherForm(instance=teacher.user)
    return render(request, 'edit_teacher.html', {'form': form})

@login_required
def manage_teachers(request):
    # Ensure only schools can access this page
    if request.user.user_type != 'school':
        return redirect('login')

    # Fetch all teachers associated with the logged-in school
    school = request.user.school
    teachers = Teacher.objects.filter(school=school)

    return render(request, 'manage_teachers.html', {'teachers': teachers})

# Helper function to check user type
def is_school(user):
    return user.user_type == 'school'

def is_teacher(user):
    return user.user_type == 'teacher'

def is_student(user):
    return user.user_type == 'student'

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
@user_passes_test(is_school, login_url='login')
def school_dashboard(request):
    school = request.user.school
    teachers = Teacher.objects.filter(school=school)
    students = Student.objects.filter(school=school)

    return render(request, 'school_dashboard.html', {
        'school': school,
        'teachers': teachers,
        'students': students,
    })


# Teacher Dashboard View
@login_required
@user_passes_test(is_teacher, login_url='login')
def teacher_dashboard(request):
    # Get the logged-in user
    user = request.user

    # Get the teacher profile associated with the user
    try:
        teacher = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        # Handle the case where the teacher profile does not exist
        teacher = None

    # Get the profile picture URL (handle cases where it's missing)
    profile_pic_url = user.profile_pic.url if user.profile_pic else None

    # Pass context to the template
    context = {
        'teacher': teacher,
        'profile_pic_url': profile_pic_url,
    }

    return render(request, 'teacher_dashboard.html', context)

# Student Dashboard View
@login_required
@user_passes_test(is_student, login_url='login')
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

# Login View
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
@login_required
@user_passes_test(is_school, login_url='login')
def add_teacher(request):
    if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'A user with this email already exists.')
                return redirect('add_teacher')  # Redirect back to the form

            # Create User for Teacher
            teacher_user = User.objects.create_user(
                email=email,
                password=form.cleaned_data['password'],
                user_type='teacher'
            )

            # Create Teacher Profile
            school = request.user.school  # Assuming the logged-in user is a school
            Teacher.objects.create(
                user=teacher_user,
                school=school,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            messages.success(request, 'Teacher added successfully.')
            return redirect('school_dashboard')  # Redirect to the list of teachers

    else:
        form = AddTeacherForm()

    return render(request, 'add_teacher.html', {'form': form})

# Add Student View
@login_required
@user_passes_test(is_school, login_url='login')
def add_student(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            # Create User for Student
            student_user = User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                user_type='student'
            )

            # Create Student Profile
            student = Student.objects.create(
                user=student_user,
                school=request.user.school,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            # Send email to student with their credentials
            send_mail(
                'Your account has been created',
                f'Your email: {student_user.email}\nYour password: {form.cleaned_data["password"]}',
                settings.EMAIL_HOST_USER,
                [student_user.email],
                fail_silently=False,
            )

            return redirect('school_dashboard')
    else:
        form = AddStudentForm()
    return render(request, 'add_student.html', {'form': form})

# Teacher Password Change View
@login_required
@user_passes_test(is_teacher, login_url='login')
def teacher_change_password(request):
    if request.method == 'POST':
        form = TeacherPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherPasswordChangeForm(request.user)
    return render(request, 'teacher_change_password.html', {'form': form})

# Student Password Change View
@login_required
@user_passes_test(is_student, login_url='login')
def student_change_password(request):
    if request.method == 'POST':
        form = StudentPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = StudentPasswordChangeForm(request.user)
    return render(request, 'student_change_password.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('login')