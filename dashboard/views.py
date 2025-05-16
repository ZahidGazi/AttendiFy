from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from datetime import date

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
    return render(request, 'contents/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def attendance(request):
    default_date = date.today().isoformat()
    return render(request, 'contents/attendance.html', {'default_date': default_date})

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
