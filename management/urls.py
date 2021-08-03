from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_form, name='employee_insert'), # get and post request for inserting
    path('<int:id>', views.employee_form, name='employee_update'), # get and post request for updating
    path('delete/<int:id>/',views.employee_delete,name='employee_delete'),
    path('list', views.employee_list, name='employee_list'), # get request to retrive and display records
    path('collect_data/<int:id>', views.collect_data, name='collect_data'),
    path('train', views.train_system, name='train_system'),
    path('recognize', views.recognize_face, name='recognize_face'),
    path('view_attendance', views.attendance_list, name='attendance_list'),
    path('attendance/<int:id>', views.attendance_form, name='attendance_update'),
    path('delete_attendance/<int:id>/',views.attendance_delete,name='attendance_delete'),
    path('attendance', views.attendance_form, name='attendance_insert')
]