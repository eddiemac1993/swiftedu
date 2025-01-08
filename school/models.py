from django.db import models

class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

class Student(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE)