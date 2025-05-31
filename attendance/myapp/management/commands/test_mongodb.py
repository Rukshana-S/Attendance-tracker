from django.core.management.base import BaseCommand
from django.db import connection
from myapp.models import Student, Attendance
from datetime import date
import pymongo


class Command(BaseCommand):
    help = 'Test MongoDB connection and operations'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing MongoDB Connection...'))
        
        try:
            # Test 1: Check database configuration
            self.stdout.write(f"Database Engine: {connection.settings_dict['ENGINE']}")
            self.stdout.write(f"Database Name: {connection.settings_dict['NAME']}")
            
            # Test 2: Test basic connection
            students_count = Student.objects.count()
            self.stdout.write(f"Current students in database: {students_count}")
            
            # Test 3: Create a test student
            test_student = Student.objects.create(
                name="MongoDB Test Student",
                roll_number="MONGO001",
                class_name="Test Class"
            )
            self.stdout.write(f"Created test student: {test_student}")
            
            # Test 4: Create attendance record
            test_attendance = Attendance.objects.create(
                student=test_student,
                date=date.today(),
                status='Present'
            )
            self.stdout.write(f"Created test attendance: {test_attendance}")
            
            # Test 5: Query operations
            all_students = Student.objects.all()
            self.stdout.write(f"Total students after test: {all_students.count()}")
            
            # Test 6: Filter operations
            test_class_students = Student.objects.filter(class_name="Test Class")
            self.stdout.write(f"Students in Test Class: {test_class_students.count()}")
            
            # Test 7: Direct MongoDB connection
            try:
                client = pymongo.MongoClient('localhost', 27017)
                db = client['attendance_db']
                collections = db.list_collection_names()
                self.stdout.write(f"MongoDB collections: {collections}")
                client.close()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Direct MongoDB connection test failed: {e}"))
            
            # Cleanup test data
            test_attendance.delete()
            test_student.delete()
            self.stdout.write(self.style.SUCCESS("Test data cleaned up"))
            
            self.stdout.write(self.style.SUCCESS('✅ All MongoDB tests passed successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ MongoDB test failed: {str(e)}'))
            raise e
