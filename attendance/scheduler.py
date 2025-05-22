from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from attendance.models import AttendanceSchedule
from attendance.take_attendance import take_attendance
import atexit
from datetime import timedelta, datetime
import logging

logger = logging.getLogger("scheduler")

def run_scheduled_attendance():
    now = timezone.localtime()
    logger.info(now)
    today = now.date()
    current_time = now.time().replace(second=0, microsecond=0)
    window_minutes = 2  # How many minutes back to check
    window_start = (now - timedelta(minutes=window_minutes)).time().replace(second=0, microsecond=0)
    window_end = current_time
    
    if window_start < window_end:
        schedules = AttendanceSchedule.objects.filter(date=today, time__gte=window_start, time__lte=window_end)
    else:
        # If window_start > window_end,,, it means we've wrapped past midnight,,, fixed after lot of tries lol
        schedules = AttendanceSchedule.objects.filter(date=today, time__gte=window_start) | AttendanceSchedule.objects.filter(date=today, time__lte=window_end)
    for schedule in schedules.distinct():
        logger.info(f"taking attandance for {schedule.camera.id} and course {schedule.course.id} at {schedule.time}")
        # Ensure for_time is a time object, not a string
        status, msg = take_attendance(schedule.camera.id, schedule.course.id, for_date=schedule.date)
        if status:
            logger.info(f"Attendance taken for camera {schedule.camera.id} and course {schedule.course.id} at {schedule.time}")
            schedule.delete()  # Remove the schedule after completion.......
        else:
            logger.info(f"Failed to take attendance for camera {schedule.camera.id} and course {schedule.course.id}: {msg}")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_scheduled_attendance, 'interval', minutes=1, name='attendance_scheduler', max_instances=1)
    scheduler.start()
    logger.info("Scheduler Started...")
    atexit.register(lambda: scheduler.shutdown())
