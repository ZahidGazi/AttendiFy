from django.db import models

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.username}"

class ClassRoom(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

class Camera(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    class_assigned = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name='cameras')
    ip_address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.location} - {self.class_assigned}"

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    student_class = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    roll_number = models.CharField(max_length=50)
    face_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student_class', 'roll_number')

    def __str__(self):
        return f"{self.id} - {self.name} - {self.student_class} - {self.roll_number}"

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    date = models.DateField(default=None, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.status} - {self.date}"

# NOTE: To start Student.id at 10000, you must set the sequence in the database after migration.
# For PostgreSQL: ALTER SEQUENCE attendance_student_id_seq RESTART WITH 10000;
# For SQLite: UPDATE sqlite_sequence SET seq = 9999 WHERE name = 'attendance_student';