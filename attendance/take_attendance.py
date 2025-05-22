import os
import cv2
import numpy as np
import face_recognition
from django.utils import timezone
from datetime import datetime, date
from django.db import transaction
import logging

from attendance.models import Attendance, Student, Camera, Course

logger = logging.getLogger("recognition")


def parse_camera_address(address):
    """Return int for webcam index, or str for URL/RTSP."""
    try:
        return int(address)
    except (ValueError, TypeError):
        return str(address)


def take_attendance(camera_id, course_id, for_date=None, for_time=None, duration=10):
    """Take attendance for a course using a camera.
    Args:
        camera_id (int): ID of the camera
        course_id (int): ID of the course
        for_date (str or date): Date for attendance (default: today)
        for_time (str or time): Time for attendance (default: now)
        duration (int): Duration in seconds to run recognition (default: 10)
        Returns: tuple[bool: status, str: message]"""
    try:
        camera = Camera.objects.get(id=camera_id)
        course = Course.objects.get(id=course_id)
    except (Camera.DoesNotExist, Course.DoesNotExist):
        msg = f"Camera or Course not found: camera_id={camera_id}, course_id={course_id}"
        logger.error(msg)
        return False, msg

    if for_date is None:
        for_date = date.today()
    elif isinstance(for_date, str):
        try:
            for_date = datetime.strptime(for_date, "%Y-%m-%d").date()
        except ValueError:
            logger.error(f"Invalid date format: {for_date}")
            return False, f"Invalid date format: {for_date}"

    if for_time is None:
        for_time = datetime.now().time()

    students = Student.objects.filter(student_class=course)
    face_data_dir = os.path.join('face_data')

    known_encodings = []
    known_ids = []
    for student in students:
        img_path = os.path.join(face_data_dir, f"{student.id}.jpg")
        if os.path.exists(img_path):
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_ids.append(student.id)

    recognized_ids = set()
    
    video = cv2.VideoCapture(parse_camera_address(camera.address))
    if not video.isOpened():
        video.release()
        msg = f"Camera could not be opened, camera Adress: {camera.address}"
        logger.error(msg)
        return False, msg

    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < duration:
        ret, frame = video.read()
        if not ret or frame is None or frame.shape[0] == 0:
            msg = f"Camera could not read frame, camera Adress: {camera.address}"
            logger.error(msg)
            continue

        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        rgb_small_frame = np.ascontiguousarray(rgb_small_frame)

        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            if True in matches:
                index = matches.index(True)
                recognized_ids.add(known_ids[index])

    video.release()
    logger.info(f"Recognition complete. Recognized IDs: {recognized_ids}")
    if not recognized_ids:
        msg = f"Recognition failed or no faces detected"
        logger.info(msg)
        return False, msg

    aware_timestamp = timezone.make_aware(datetime.combine(for_date, for_time))

    try:
        with transaction.atomic():
            for student in students:
                status = 'Present' if student.id in recognized_ids else 'Absent'
                Attendance.objects.update_or_create(
                    student=student,
                    date=for_date,
                    defaults={
                        'status': status,
                        'camera': camera,
                        'timestamp': aware_timestamp
                    }
                )
        logger.info(f"Attendance taken for course={course.name}, camera={camera.name}, date={for_date}")
        return True, "Attendance taken successfully"
    except Exception as e:
        logger.error(f"Attendance error: {e}")
        return False, str(e)
