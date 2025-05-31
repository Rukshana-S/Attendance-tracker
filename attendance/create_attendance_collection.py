#!/usr/bin/env python3
"""
Create and populate the new Student Attendance Collection
This script creates sample attendance data with date and time
"""
import os
import sys
import django
from datetime import datetime, date, time, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
django.setup()

from myapp.models import StudentAttendanceRecord, Student
from django.utils import timezone
import pymongo

def create_sample_students():
    """Create sample students if they don't exist"""
    
    print("👥 Creating Sample Students...")
    
    sample_students = [
        {"name": "RUKSHANA S", "roll_number": "CSE001", "class_name": "CSE-A", "email": "rukshana@college.edu"},
        {"name": "ARJUN KUMAR", "roll_number": "CSE002", "class_name": "CSE-A", "email": "arjun@college.edu"},
        {"name": "PRIYA SHARMA", "roll_number": "CSE003", "class_name": "CSE-A", "email": "priya@college.edu"},
        {"name": "RAHUL VERMA", "roll_number": "CSE004", "class_name": "CSE-B", "email": "rahul@college.edu"},
        {"name": "SNEHA PATEL", "roll_number": "CSE005", "class_name": "CSE-B", "email": "sneha@college.edu"},
        {"name": "VIKRAM SINGH", "roll_number": "CSE006", "class_name": "CSE-A", "email": "vikram@college.edu"},
        {"name": "ANITA REDDY", "roll_number": "CSE007", "class_name": "CSE-B", "email": "anita@college.edu"},
        {"name": "KARTHIK RAO", "roll_number": "CSE008", "class_name": "CSE-A", "email": "karthik@college.edu"},
    ]
    
    created_students = []
    
    for student_data in sample_students:
        # Check if student already exists in Student model
        student, created = Student.objects.get_or_create(
            roll_number=student_data["roll_number"],
            defaults={
                'name': student_data["name"],
                'class_name': student_data["class_name"]
            }
        )
        
        if created:
            print(f"   ✅ Created: {student.name} ({student.roll_number})")
        else:
            print(f"   📋 Exists: {student.name} ({student.roll_number})")
        
        created_students.append({
            'name': student_data["name"],
            'roll_number': student_data["roll_number"],
            'class_name': student_data["class_name"],
            'email': student_data["email"]
        })
    
    return created_students

def create_attendance_records(students):
    """Create sample attendance records for the past week"""
    
    print(f"\n📊 Creating Attendance Records...")
    
    # Define subjects
    subjects = [
        {"name": "Data Structures", "code": "CS201"},
        {"name": "Database Management", "code": "CS202"},
        {"name": "Computer Networks", "code": "CS203"},
        {"name": "Operating Systems", "code": "CS204"},
        {"name": "Software Engineering", "code": "CS205"},
    ]
    
    # Define session types and times
    sessions = [
        {"type": "Morning", "time": time(9, 0)},
        {"type": "Afternoon", "time": time(14, 0)},
        {"type": "Lab", "time": time(10, 30)},
        {"type": "Tutorial", "time": time(15, 30)},
    ]
    
    # Define attendance statuses with probabilities
    statuses = ["Present", "Present", "Present", "Present", "Absent", "Late", "Present"]
    
    # Create records for the past 7 days
    records_created = 0
    
    for day_offset in range(7):
        attendance_date = date.today() - timedelta(days=day_offset)
        
        # Skip weekends
        if attendance_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
            continue
        
        print(f"   📅 Creating records for {attendance_date}")
        
        for student in students:
            for subject in subjects:
                for session in sessions:
                    # Random chance of having this session (not all subjects every day)
                    if random.random() < 0.7:  # 70% chance
                        
                        # Create attendance record
                        try:
                            attendance_status = random.choice(statuses)
                            
                            # Add some randomness to time (±15 minutes)
                            base_time = session["time"]
                            minutes_offset = random.randint(-15, 15)
                            actual_time = (datetime.combine(date.today(), base_time) + 
                                         timedelta(minutes=minutes_offset)).time()
                            
                            record = StudentAttendanceRecord.objects.create(
                                student_name=student["name"],
                                student_roll_number=student["roll_number"],
                                student_class=student["class_name"],
                                student_email=student["email"],
                                attendance_status=attendance_status,
                                attendance_date=attendance_date,
                                attendance_time=actual_time,
                                attendance_datetime=datetime.combine(attendance_date, actual_time),
                                session_type=session["type"],
                                subject_name=subject["name"],
                                subject_code=subject["code"],
                                marked_by="System Admin",
                                location=f"Room {random.randint(101, 205)}",
                                remarks="Auto-generated sample data" if random.random() < 0.3 else None
                            )
                            
                            records_created += 1
                            
                        except Exception as e:
                            # Skip if duplicate (unique constraint)
                            if "duplicate" not in str(e).lower():
                                print(f"      ⚠️  Error creating record: {e}")
    
    print(f"   ✅ Created {records_created} attendance records")
    return records_created

def verify_collection():
    """Verify the new collection in MongoDB"""
    
    print(f"\n🔍 Verifying MongoDB Collection...")
    
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient('localhost', 27017)
        db = client['attendance_db']
        
        # Check if collection exists
        collections = db.list_collection_names()
        
        if 'Attendancetracker.student_attendance' in collections:
            print("   ✅ Attendancetracker.student_attendance collection found!")
            
            collection = db['Attendancetracker.student_attendance']
            count = collection.count_documents({})
            print(f"   📊 Total attendance records: {count}")
            
            if count > 0:
                print(f"   📄 Sample records:")
                
                # Show recent records
                recent_records = list(collection.find({}).sort("attendance_date", -1).limit(5))
                
                for i, record in enumerate(recent_records, 1):
                    print(f"      {i}. {record.get('student_name')} ({record.get('student_roll_number')})")
                    print(f"         📅 {record.get('attendance_date')} ⏰ {record.get('attendance_time')}")
                    print(f"         📚 {record.get('subject_name')} - {record.get('attendance_status')}")
                    print(f"         🏫 {record.get('session_type')} session in {record.get('location')}")
                    print()
            
        else:
            print("   ❌ Collection not found")
            print(f"   📁 Available collections: {collections}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"   ❌ MongoDB verification failed: {e}")
        return False

def show_attendance_statistics():
    """Show attendance statistics from Django ORM"""
    
    print(f"\n📈 Attendance Statistics...")
    
    try:
        total_records = StudentAttendanceRecord.objects.count()
        print(f"   📊 Total Records: {total_records}")
        
        if total_records > 0:
            # Status breakdown
            from django.db.models import Count
            
            status_counts = StudentAttendanceRecord.objects.values('attendance_status').annotate(
                count=Count('attendance_status')
            ).order_by('-count')
            
            print(f"   📋 Status Breakdown:")
            for status in status_counts:
                print(f"      • {status['attendance_status']}: {status['count']} records")
            
            # Class breakdown
            class_counts = StudentAttendanceRecord.objects.values('student_class').annotate(
                count=Count('student_class')
            ).order_by('-count')
            
            print(f"   🏫 Class Breakdown:")
            for class_data in class_counts:
                print(f"      • {class_data['student_class']}: {class_data['count']} records")
            
            # Recent records
            print(f"   📅 Recent Records:")
            recent = StudentAttendanceRecord.objects.order_by('-attendance_date', '-attendance_time')[:3]
            
            for record in recent:
                print(f"      • {record.student_name} - {record.attendance_date} - {record.attendance_status}")
        
    except Exception as e:
        print(f"   ❌ Statistics error: {e}")

def create_web_viewer_for_attendance():
    """Create a web viewer for the attendance data"""
    
    print(f"\n🌐 Creating Attendance Web Viewer...")
    
    try:
        # Get recent attendance data
        records = StudentAttendanceRecord.objects.order_by('-attendance_date', '-attendance_time')[:20]
        
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Student Attendance Records</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; text-align: center; }}
        .stats {{ background: #e8f5e8; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .record-card {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; background: #fafafa; }}
        .record-header {{ font-weight: bold; color: #2c5aa0; font-size: 16px; }}
        .record-detail {{ margin: 5px 0; display: inline-block; margin-right: 20px; }}
        .label {{ font-weight: bold; color: #555; }}
        .status-present {{ color: #4CAF50; font-weight: bold; }}
        .status-absent {{ color: #f44336; font-weight: bold; }}
        .status-late {{ color: #ff9800; font-weight: bold; }}
        .refresh-btn {{ background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Student Attendance Records</h1>
        
        <div class="stats">
            <h3>📈 Collection Information</h3>
            <p><span class="label">Collection:</span> Attendancetracker.student_attendance</p>
            <p><span class="label">Total Records:</span> {StudentAttendanceRecord.objects.count()}</p>
            <p><span class="label">Last Updated:</span> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Data</button>
        
        <h3>📋 Recent Attendance Records:</h3>
        
        <table>
            <thead>
                <tr>
                    <th>Student</th>
                    <th>Roll Number</th>
                    <th>Class</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Status</th>
                    <th>Session</th>
                    <th>Subject</th>
                    <th>Location</th>
                </tr>
            </thead>
            <tbody>
'''
        
        for record in records:
            status_class = f"status-{record.attendance_status.lower()}"
            html_content += f'''
                <tr>
                    <td>{record.student_name}</td>
                    <td>{record.student_roll_number}</td>
                    <td>{record.student_class}</td>
                    <td>{record.attendance_date}</td>
                    <td>{record.attendance_time}</td>
                    <td><span class="{status_class}">{record.attendance_status}</span></td>
                    <td>{record.session_type}</td>
                    <td>{record.subject_name}</td>
                    <td>{record.location or 'N/A'}</td>
                </tr>
'''
        
        html_content += '''
            </tbody>
        </table>
    </div>
</body>
</html>'''
        
        with open('student_attendance_viewer.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("   ✅ Created: student_attendance_viewer.html")
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to create web viewer: {e}")
        return False

def main():
    """Main function to create the attendance collection and data"""
    
    print("🚀 CREATING STUDENT ATTENDANCE COLLECTION")
    print("=" * 60)
    
    # Step 1: Create sample students
    students = create_sample_students()
    
    # Step 2: Create attendance records
    records_count = create_attendance_records(students)
    
    # Step 3: Verify MongoDB collection
    verify_collection()
    
    # Step 4: Show statistics
    show_attendance_statistics()
    
    # Step 5: Create web viewer
    create_web_viewer_for_attendance()
    
    # Step 6: Summary
    print(f"\n🎉 ATTENDANCE COLLECTION SETUP COMPLETE!")
    print("=" * 50)
    print("✅ New MongoDB collection created: Attendancetracker.student_attendance")
    print(f"✅ Sample students created: {len(students)}")
    print(f"✅ Attendance records created: {records_count}")
    print("✅ Web viewer created: student_attendance_viewer.html")
    print()
    print("📋 What you can do now:")
    print("1. 🌐 Open student_attendance_viewer.html in browser")
    print("2. 📱 Use MongoDB Compass to view: Attendancetracker.student_attendance")
    print("3. 📊 Access Django admin: http://localhost:8000/admin/")
    print("4. 🔍 View 'Student Attendance Records' in admin panel")

if __name__ == "__main__":
    main()
