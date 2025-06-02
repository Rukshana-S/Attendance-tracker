from djongo import models
from django.utils import timezone


class AttendanceUser(models.Model):
    """Custom User model that stores data in Attendancetracker.users collection"""

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    password_hash = models.CharField(max_length=255)  # Store hashed password
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Attendancetracker.users'  # This sets the MongoDB collection name
        verbose_name = 'Attendance User'
        verbose_name_plural = 'Attendance Users'

    def __str__(self):
        return self.username

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between"""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user"""
        return self.first_name


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    class_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])


class StudentAttendanceRecord(models.Model):
    """Enhanced attendance tracking with detailed date/time information"""

    # Student Information
    student_name = models.CharField(max_length=100)
    student_roll_number = models.CharField(max_length=20)
    student_class = models.CharField(max_length=50)
    student_email = models.EmailField(blank=True, null=True)

    # Attendance Details
    attendance_status = models.CharField(
        max_length=20,
        choices=[
            ('Present', 'Present'),
            ('Absent', 'Absent'),
            ('Late', 'Late'),
            ('Excused', 'Excused'),
            ('Partial', 'Partial')
        ],
        default='Present'
    )

    # Date and Time Information
    attendance_date = models.DateField(default=timezone.now)
    attendance_time = models.TimeField(default=timezone.now)
    attendance_datetime = models.DateTimeField(default=timezone.now)

    # Session Information
    session_type = models.CharField(
        max_length=30,
        choices=[
            ('Morning', 'Morning Session'),
            ('Afternoon', 'Afternoon Session'),
            ('Evening', 'Evening Session'),
            ('Full Day', 'Full Day'),
            ('Lecture', 'Lecture'),
            ('Lab', 'Lab Session'),
            ('Tutorial', 'Tutorial')
        ],
        default='Full Day'
    )

    # Subject/Course Information
    subject_name = models.CharField(max_length=100, blank=True, null=True)
    subject_code = models.CharField(max_length=20, blank=True, null=True)

    # Additional Information
    marked_by = models.CharField(max_length=100)  # Teacher/Admin who marked attendance
    remarks = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)  # Classroom, Lab, etc.

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Attendancetracker.student_attendance'  # MongoDB collection name
        verbose_name = 'Student Attendance Record'
        verbose_name_plural = 'Student Attendance Records'
        # Ensure unique attendance per student per date per session
        unique_together = ['student_roll_number', 'attendance_date', 'session_type', 'subject_code']

    def __str__(self):
        return f"{self.student_name} ({self.student_roll_number}) - {self.attendance_date} - {self.attendance_status}"

    def get_attendance_summary(self):
        """Get a summary of the attendance record"""
        return {
            'student': f"{self.student_name} ({self.student_roll_number})",
            'date': self.attendance_date.strftime('%Y-%m-%d'),
            'time': self.attendance_time.strftime('%H:%M:%S'),
            'status': self.attendance_status,
            'session': self.session_type,
            'subject': self.subject_name or 'General',
            'marked_by': self.marked_by
        }

    @classmethod
    def mark_attendance(cls, student_data, attendance_data, marked_by_user):
        """Class method to mark attendance for a student"""
        return cls.objects.create(
            student_name=student_data.get('name'),
            student_roll_number=student_data.get('roll_number'),
            student_class=student_data.get('class_name'),
            student_email=student_data.get('email'),
            attendance_status=attendance_data.get('status', 'Present'),
            attendance_date=attendance_data.get('date', timezone.now().date()),
            attendance_time=attendance_data.get('time', timezone.now().time()),
            session_type=attendance_data.get('session_type', 'Full Day'),
            subject_name=attendance_data.get('subject_name'),
            subject_code=attendance_data.get('subject_code'),
            marked_by=marked_by_user,
            remarks=attendance_data.get('remarks'),
            location=attendance_data.get('location')
        )
