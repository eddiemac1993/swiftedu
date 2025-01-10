from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs (login/logout)
    path('', views.login_view, name='login'),  # Use custom login view
    path('logout/', views.custom_logout, name='logout'),
    
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
    
    path('manage-teachers/', views.manage_teachers, name='manage_teachers'),
    path('edit-teacher/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('delete-teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('manage-students/', views.manage_students, name='manage_students'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
]