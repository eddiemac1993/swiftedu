from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, School, Teacher, Student

class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('email', 'user_type', 'phone_number', 'profile_pic')

    # Fields to include in the add/edit forms
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('user_type', 'phone_number', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to include in the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'phone_number', 'profile_pic'),
        }),
    )

    # Override the ordering attribute
    ordering = ('email',)  # Use 'email' instead of 'username'

# Register the User model with the CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(School)
admin.site.register(Teacher)
admin.site.register(Student)