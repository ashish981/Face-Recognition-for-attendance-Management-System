from django.db import models

# Create your models here.

class Group(models.Model):
    group = models.CharField(max_length=10)

    def __str__(self):
        return self.group

class Employee(models.Model):
    name = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=10)
    gender_choice = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=gender_choice, default='Male')
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    photo_status = models.IntegerField(default=0)

class Attendance(models.Model):
    name = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=10)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    date = models.DateField()
    status_choice = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
    )
    attendance_status = models.CharField(max_length=10, choices=status_choice, default='Male')
