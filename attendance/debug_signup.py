#!/usr/bin/env python3
"""
Debug script to test signup functionality and identify issues
"""
import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from myapp.models import AttendanceUser
import pymongo

def debug_signup_process():
    """Debug the signup process step by step"""
    
    print("🔍 DEBUG: Signup Process")
    print("=" * 40)
    
    # Test data
    test_username = f"debug_user_{datetime.now().strftime('%H%M%S')}"
    test_data = {
        'username': test_username,
        'first_name': 'Debug',
        'last_name': 'User',
        'email': f'{test_username}@example.com',
        'password1': 'debugpassword123',
        'password2': 'debugpassword123'
    }
    
    print(f"📝 Test Data:")
    for key, value in test_data.items():
        if 'password' not in key:
            print(f"   {key}: {value}")
    
    # Check initial state
    print(f"\n📊 Initial State:")
    django_users_before = User.objects.count()
    attendance_users_before = AttendanceUser.objects.count()
    print(f"   Django Users: {django_users_before}")
    print(f"   AttendanceUsers: {attendance_users_before}")
    
    try:
        # Test the signup view directly
        print(f"\n🧪 Testing Signup View:")
        
        client = Client()
        response = client.post('/signup/', test_data)
        
        print(f"   Response Status: {response.status_code}")
        
        if response.status_code == 200:
            # Check for errors in response
            content = response.content.decode('utf-8')
            if 'error' in content.lower():
                print("   ❌ Error found in response")
                # Extract error message
                import re
                error_match = re.search(r'<p class="error-message">(.*?)</p>', content)
                if error_match:
                    print(f"   Error: {error_match.group(1)}")
            else:
                print("   ⚠️  Form returned to signup page (no redirect)")
        elif response.status_code == 302:
            print("   ✅ Successful redirect (signup worked)")
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
        
        # Check final state
        print(f"\n📊 Final State:")
        django_users_after = User.objects.count()
        attendance_users_after = AttendanceUser.objects.count()
        print(f"   Django Users: {django_users_after} (change: +{django_users_after - django_users_before})")
        print(f"   AttendanceUsers: {attendance_users_after} (change: +{attendance_users_after - attendance_users_before})")
        
        # Check if our test user was created
        print(f"\n🔍 User Creation Check:")
        
        try:
            django_user = User.objects.get(username=test_username)
            print(f"   ✅ Django User found: {django_user.username}")
        except User.DoesNotExist:
            print(f"   ❌ Django User not found: {test_username}")
        
        try:
            attendance_user = AttendanceUser.objects.get(username=test_username)
            print(f"   ✅ AttendanceUser found: {attendance_user.username}")
            print(f"   📧 Email: {attendance_user.email}")
            print(f"   👤 Name: {attendance_user.get_full_name()}")
        except AttendanceUser.DoesNotExist:
            print(f"   ❌ AttendanceUser not found: {test_username}")
        
        # Check MongoDB directly
        print(f"\n🗄️  MongoDB Direct Check:")
        
        try:
            client_mongo = pymongo.MongoClient('localhost', 27017)
            db = client_mongo['attendance_db']
            
            # Check if collection exists
            collections = db.list_collection_names()
            if 'Attendancetracker.users' in collections:
                print("   ✅ Attendancetracker.users collection exists")
                
                count = db['Attendancetracker.users'].count_documents({})
                print(f"   📊 Total documents: {count}")
                
                # Look for our test user
                user_doc = db['Attendancetracker.users'].find_one({"username": test_username})
                if user_doc:
                    print(f"   ✅ Test user found in MongoDB")
                    print(f"   📄 Document: {user_doc.get('username')} - {user_doc.get('email')}")
                else:
                    print(f"   ❌ Test user not found in MongoDB")
                
                # Show all users in collection
                print(f"\n   📋 All users in Attendancetracker.users:")
                all_docs = list(db['Attendancetracker.users'].find({}))
                for doc in all_docs:
                    print(f"      • {doc.get('username')} - {doc.get('email')}")
                
            else:
                print("   ❌ Attendancetracker.users collection not found")
                print(f"   📁 Available collections: {collections}")
            
            client_mongo.close()
            
        except Exception as e:
            print(f"   ❌ MongoDB check failed: {e}")
        
        # Cleanup
        print(f"\n🧹 Cleanup:")
        try:
            User.objects.filter(username=test_username).delete()
            AttendanceUser.objects.filter(username=test_username).delete()
            print("   ✅ Test data cleaned up")
        except Exception as e:
            print(f"   ⚠️  Cleanup warning: {e}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_view_code():
    """Check if there are any issues with the view code"""
    
    print(f"\n🔍 Checking View Code:")
    
    try:
        from myapp.views import user_signup
        print("   ✅ user_signup view imported successfully")
        
        # Check if AttendanceUser is imported
        import inspect
        source = inspect.getsource(user_signup)
        
        if 'AttendanceUser' in source:
            print("   ✅ AttendanceUser referenced in view")
        else:
            print("   ❌ AttendanceUser not found in view code")
        
        if 'AttendanceUser.objects.create' in source:
            print("   ✅ AttendanceUser.objects.create found in view")
        else:
            print("   ❌ AttendanceUser.objects.create not found in view")
        
    except Exception as e:
        print(f"   ❌ View check failed: {e}")

def manual_user_creation_test():
    """Test manual user creation to isolate the issue"""
    
    print(f"\n🧪 Manual User Creation Test:")
    
    test_username = f"manual_test_{datetime.now().strftime('%H%M%S')}"
    
    try:
        from django.contrib.auth.hashers import make_password
        from django.utils import timezone
        
        # Create AttendanceUser manually
        attendance_user = AttendanceUser.objects.create(
            username=test_username,
            email=f"{test_username}@example.com",
            first_name="Manual",
            last_name="Test",
            password_hash=make_password("testpassword123"),
            is_active=True,
            date_joined=timezone.now()
        )
        
        print(f"   ✅ Manual AttendanceUser created: {attendance_user.username}")
        print(f"   🆔 ID: {attendance_user.id}")
        
        # Check MongoDB
        client_mongo = pymongo.MongoClient('localhost', 27017)
        db = client_mongo['attendance_db']
        
        user_doc = db['Attendancetracker.users'].find_one({"username": test_username})
        if user_doc:
            print(f"   ✅ Manual user found in MongoDB")
        else:
            print(f"   ❌ Manual user not found in MongoDB")
        
        client_mongo.close()
        
        # Cleanup
        attendance_user.delete()
        print(f"   ✅ Manual test user cleaned up")
        
    except Exception as e:
        print(f"   ❌ Manual creation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Signup Debug Session")
    print("=" * 50)
    
    # Check view code
    check_view_code()
    
    # Test manual creation
    manual_user_creation_test()
    
    # Debug signup process
    debug_signup_process()
    
    print("\n🎯 Debug session completed")
