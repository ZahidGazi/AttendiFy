from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from datetime import date
from attendance.models import Student, Attendance, ClassRoom
from datetime import date, timedelta
from django.db.models import Count, Q
from django.http import HttpResponse
import csv
import io
import openpyxl

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard-home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard_home(request):
    selected_class_id = request.GET.get('class')
    today = date.today()
    week_days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    week_days_labels = [d.strftime('%a') for d in week_days]

    # Filter students by class if selected
    students = Student.objects.all()
    if selected_class_id:
        students = students.filter(student_class_id=selected_class_id)

    total_students = students.count()
    today_attendance = Attendance.objects.filter(student__in=students, date=today, status='Present').count()
    absent_today = total_students - today_attendance

    # Attendance trend for the past 7 days
    attendance_trend = [
        Attendance.objects.filter(student__in=students, date=day, status='Present').count()
        for day in week_days
    ]

    # Pie chart data
    present_count = today_attendance
    absent_count = Attendance.objects.filter(student__in=students, date=today, status='Absent').count()
    pie_data = [present_count, absent_count]

    # Top 3 students with best attendance (most presents)
    top_students = students.annotate(presents=Count('attendance', filter=Q(attendance__status='Present'))).order_by('-presents')[:3]
    # Top 3 frequent absentees
    frequent_absentees = students.annotate(absents=Count('attendance', filter=Q(attendance__status='Absent'))).order_by('-absents')[:3]

    classes = ClassRoom.objects.all()

    context = {
        'total_students': total_students,
        'today_attendance': today_attendance,
        'absent_today': absent_today,
        'attendance_trend': attendance_trend,
        'week_days_labels': week_days_labels,
        'present_count': present_count,
        'absent_count': absent_count,
        'pie_data': pie_data,
        'top_students': top_students,
        'frequent_absentees': frequent_absentees,
        'classes': classes,
        'selected_class_id': selected_class_id,
    }
    return render(request, 'contents/dashboard.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def attendance(request):
    from attendance.models import Student, Attendance, ClassRoom
    # Get filter params
    class_id = request.GET.get('class')
    date_str = request.GET.get('date')
    if date_str:
        from datetime import datetime
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            selected_date = date.today()
    else:
        selected_date = date.today()

    students = Student.objects.all().select_related('student_class')
    if class_id:
        students = students.filter(student_class_id=class_id)

    #POST: update attendance
    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status in ['Present', 'Absent']:
                Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    defaults={'status': status}
                )

    # Get attendance records for the selected date
    attendance_records = Attendance.objects.filter(student__in=students, date=selected_date)
    attendance_map = {a.student.id: a.status for a in attendance_records}
    for student in students:
        student.attendance_status = attendance_map.get(student.id, "")

    # For class dropdown
    classes = ClassRoom.objects.all()

    context = {
        'default_date': selected_date.isoformat(),
        'students': students,
        'attendance_map': attendance_map,
        'classes': classes,
        'selected_class_id': class_id or '',
    }
    return render(request, 'contents/attendance.html', context)

@login_required(login_url='login')
def students(request):
    return render(request, 'contents/students.html')

@login_required(login_url='login')
def staff(request):
    return render(request, 'contents/staff.html')

@login_required(login_url='login')
def alerts(request):
    return render(request, 'contents/alerts.html')

@login_required(login_url='login')
def settings(request):
    return render(request, 'contents/settings.html')

@login_required(login_url='login')
def attendance_download(request):
    from attendance.models import Student, Attendance, ClassRoom
    class_id = request.GET.get('class')
    date_str = request.GET.get('date')
    filetype = request.GET.get('filetype', 'csv')
    if date_str:
        from datetime import datetime
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            from datetime import date
            selected_date = date.today()
    else:
        from datetime import date
        selected_date = date.today()

    classroom_name = "all_classes"
    students = Student.objects.all().select_related('student_class')
    if class_id:
        students = students.filter(student_class_id=class_id)
        classroom = ClassRoom.objects.filter(id=class_id).first()
        if classroom:
            classroom_name = classroom.name.replace(" ", "_")

    attendance_records = Attendance.objects.filter(student__in=students, date=selected_date)
    attendance_map = {a.student.id: a.status for a in attendance_records}

    filename = f"{classroom_name}_attendance_{selected_date}"
    headers = ['Student ID', 'Name', 'Roll No', 'Status']
    data_rows = [
        [student.id, student.name, student.roll_number, attendance_map.get(student.id, '')]
        for student in students
    ]

    if filetype == 'xlsx':
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(headers)
        for row in data_rows:
            ws.append(row)
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        return response
    else:  # default to CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        writer = csv.writer(response)
        writer.writerow(headers)
        for row in data_rows:
            writer.writerow(row)
        return response
