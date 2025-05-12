from django.db import models
from dashboard.models import Student

class Camera(models.Model):
    location = models.CharField(max_length=100)
    class_assigned = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.class_assigned}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Manual', 'Manual'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.status} - {self.timestamp}"
