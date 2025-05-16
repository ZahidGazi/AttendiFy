from django.contrib import admin
from .models import Admin, ClassRoom, Student, Camera, Attendance

admin.site.register(Admin)
admin.site.register(ClassRoom)
admin.site.register(Student)
admin.site.register(Camera)
admin.site.register(Attendance)
