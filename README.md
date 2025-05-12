# AttendiFy

Attendify is a smart, camera-powered attendance system that uses facial recognition to mark presence, flag unknown entries, and keep everything logged and visualized. It is designed to streamline attendance management for schools, colleges, and organizations.

## Features
- **Facial Recognition**: Automatically mark attendance using camera feeds.
- **Class Management**: Manage students and classes efficiently.
- **Attendance Records**: View and edit attendance records.
- **Alerts**: Flag unauthorized entries.
- **Admin Dashboard**: A user-friendly dashboard for managing the system.

## Prerequisites
- Python 3.10 or higher
- PostgreSQL database
- Virtual environment (recommended)

## Installation and Configuration

### 1. Clone the Repository
```bash
git clone https://github.com/zahidGazi/attendify.git
cd attendify
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the Database
1. Create a PostgreSQL database and user:
   ```sql
   CREATE DATABASE <your_database_name>;
   CREATE USER <your_database_user> WITH PASSWORD '<your_password>';
   GRANT ALL PRIVILEGES ON DATABASE <your_database_name> TO <your_database_user>;
   GRANT ALL ON SCHEMA public TO <your_database_user>;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO <your_database_user>;
   ```
2. Update the `.env` file with your database credentials:
   ```properties
   DB_NAME=<your_database_name>
   DB_USER=<your_database_user>
   DB_PASSWORD=<your_password>
   DB_HOST=localhost
   DB_PORT=5432
   ```

### 5. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```
Access the application at `http://127.0.0.1:8000/`.

## Folder Structure
- `app/`: Core Django project settings and configurations.
- `dashboard/`: Handles the admin dashboard and student management.
- `attendance/`: Manages attendance records and camera integration.
- `recognition/`: Facial recognition logic and related features.
- `static/`: Static files (CSS, JavaScript, images).
- `templates/`: HTML templates for the application.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## Contact
For any inquiries or support, please contact [mnuvq](https://t.me/mnuvq).
