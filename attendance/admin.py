from django.contrib import admin
from .models import Admin, Course, Student, Camera, Attendance

admin.site.register(Admin)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Camera)
admin.site.register(Attendance)
