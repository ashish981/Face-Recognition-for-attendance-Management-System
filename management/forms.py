from django import forms
from .models import Employee, Attendance


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('name','employee_id','email','phone','gender','group')
        labels = {
            'name':'Employee Name',
            'group':'Department',
            'employee_id':'Employee ID'
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm,self).__init__(*args, **kwargs)
        self.fields['group'].empty_label = "Select"

class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = ('name','employee_id','group','date','attendance_status')
        labels = {
            'name':'Employee Name',
            'employee_id':'Employee ID',
            'group':'Department',
            'attendance_status':'Attendance Status'
        }

    def __init__(self, *args, **kwargs):
        super(AttendanceForm,self).__init__(*args, **kwargs)
        self.fields['group'].empty_label = "Select"