from django.contrib import admin
from .models import Group, Employee, Attendance

# Register your models here.

admin.site.register(Employee)
admin.site.register(Group)
admin.site.register(Attendance)
