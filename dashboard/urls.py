from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_home, name='dashboard-home'),
    path('attendance', views.attendance, name='attendance'),
    path('students', views.students, name='students'),
    path('camera-and-courses', views.camera_courses, name='camera_and_courses'),
    path('schedule', views.schedule, name='schedule'),
]
