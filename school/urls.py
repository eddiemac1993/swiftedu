from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs (login/logout)
    path('', views.login_view, name='login'),  # Use custom login view
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    # Dashboard URLs
    path('school/dashboard/', views.school_dashboard, name='school_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    # School URLs
    path('school/register/', views.school_register, name='school_register'),
    path('school/add-teacher/', views.add_teacher, name='add_teacher'),
    path('school/add-student/', views.add_student, name='add_student'),

    # Teacher URLs
    path('teacher/change-password/', views.teacher_change_password, name='teacher_change_password'),
    path('student/change-password/', views.student_change_password, name='student_change_password'),
]