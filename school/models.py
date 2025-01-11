from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Custom User Model
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('school', 'School'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    username = None  # Remove the username field

    # Add phone_number and profile_pic fields
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        default='profile_pics/default.jpg'  # Default profile picture
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.user_type or self.user_type not in dict(self.USER_TYPE_CHOICES).keys():
            raise ValueError("Invalid or missing user_type")
        super().save(*args, **kwargs)

# School Model
class School(models.Model):
    """
    Represents a school in the system.
    Each school is linked to a User with user_type='school'.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='school')
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'school'], name='unique_teacher_school')
        ]

# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'school'], name='unique_student_school')
        ]

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            if instance.user_type == 'school':
                School.objects.create(user=instance)
            elif instance.user_type == 'teacher':
                Teacher.objects.create(user=instance)
            elif instance.user_type == 'student':
                Student.objects.create(user=instance)
        except Exception as e:
            logger.error(f"Error creating profile: {e}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if instance.user_type == 'school' and hasattr(instance, 'school'):
            instance.school.save()
        elif instance.user_type == 'teacher' and hasattr(instance, 'teacher'):
            instance.teacher.save()
        elif instance.user_type == 'student' and hasattr(instance, 'student'):
            instance.student.save()
    except Exception as e:
        logger.error(f"Error saving profile: {e}")