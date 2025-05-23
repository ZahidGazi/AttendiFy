# Use official Python 3.9 image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev build-essential python3-dev cmake libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev libopencv-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (if using Django staticfiles)
RUN python manage.py collectstatic --noinput

# Expose port (default Django port)
EXPOSE 8000

# Start server (use gunicorn for production)
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=3"]
