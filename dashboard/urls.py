from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_home, name='dashboard-home'),
    path('attendance', views.attendance, name='attendance'),
    path('attendance/download', views.attendance_download, name='attendance-download'),
    path('students', views.students, name='students'),
    path('staff', views.staff, name='staff'),
    path('alerts', views.alerts, name='alerts'),
    path('settings', views.settings, name='settings'),
]
