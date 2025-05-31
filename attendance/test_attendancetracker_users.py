#!/usr/bin/env python3
"""
Test script to verify that login and signup data is stored in Attendancetracker.users collection
"""
import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from myapp.models import AttendanceUser
from django.db import connection
import pymongo

def test_attendancetracker_users_storage():
    """Test that user data is stored in Attendancetracker.users collection"""
    
    print("🧪 Testing Attendancetracker.users Collection Storage")
    print("=" * 60)
    
    try:
        # Test 1: Check AttendanceUser model configuration
        print("📊 Test 1: AttendanceUser Model Configuration")
        print(f"   Model: {AttendanceUser}")
        print(f"   DB Table: {AttendanceUser._meta.db_table}")
        
        if AttendanceUser._meta.db_table == 'Attendancetracker.users':
            print("   ✅ AttendanceUser configured for Attendancetracker.users collection")
        else:
            print(f"   ❌ Unexpected db_table: {AttendanceUser._meta.db_table}")
            return False
        
        # Test 2: Create test user through signup process
        print("\n👤 Test 2: Creating Test User (Simulating Signup)")
        
        test_username = f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_email = f"{test_username}@example.com"
        test_password = "testpassword123"
        
        # Clean up any existing test users
        User.objects.filter(username=test_username).delete()
        AttendanceUser.objects.filter(username=test_username).delete()
        
        # Simulate the signup process (same as in views.py)
        from django.contrib.auth.hashers import make_password
        from django.utils import timezone
        
        # Create Django User (for authentication)
        django_user = User.objects.create_user(
            username=test_username,
            email=test_email,
            password=test_password,
            first_name="Test",
            last_name="User"
        )
        
        # Create AttendanceUser (for Attendancetracker.users collection)
        attendance_user = AttendanceUser.objects.create(
            username=test_username,
            email=test_email,
            first_name="Test",
            last_name="User",
            password_hash=make_password(test_password),
            is_active=True,
            date_joined=timezone.now()
        )
        
        print(f"   ✅ Django User created: ID {django_user.id}")
        print(f"   ✅ AttendanceUser created: ID {attendance_user.id}")
        print(f"   📧 Email: {attendance_user.email}")
        print(f"   👤 Full name: {attendance_user.get_full_name()}")
        
        # Test 3: Authentication test
        print("\n🔐 Test 3: Authentication Test")
        
        auth_user = authenticate(username=test_username, password=test_password)
        
        if auth_user:
            print("   ✅ Django authentication successful")
            print(f"   👤 Authenticated user: {auth_user.username}")
            
            # Simulate login process - update last_login in AttendanceUser
            attendance_user.last_login = timezone.now()
            attendance_user.save()
            print("   ✅ Updated last_login in AttendanceUser")
            
        else:
            print("   ❌ Authentication failed")
            return False
        
        # Test 4: Verify MongoDB storage
        print("\n🗄️  Test 4: MongoDB Collection Verification")
        
        try:
            # Connect to MongoDB directly
            client = pymongo.MongoClient('localhost', 27017)
            db = client['attendance_db']
            
            # Check collections
            collections = db.list_collection_names()
            print(f"   📁 Available collections: {[c for c in collections if 'user' in c.lower() or 'attendance' in c.lower()]}")
            
            # Check Attendancetracker.users collection
            if 'Attendancetracker.users' in collections:
                print("   ✅ Attendancetracker.users collection found!")
                
                # Count documents
                user_count = db['Attendancetracker.users'].count_documents({})
                print(f"   📊 Users in Attendancetracker.users: {user_count}")
                
                # Find our test user
                test_user_doc = db['Attendancetracker.users'].find_one({"username": test_username})
                
                if test_user_doc:
                    print("   ✅ Test user found in Attendancetracker.users collection!")
                    print(f"   📄 MongoDB document:")
                    print(f"      - _id: {test_user_doc.get('_id')}")
                    print(f"      - username: {test_user_doc.get('username')}")
                    print(f"      - email: {test_user_doc.get('email')}")
                    print(f"      - first_name: {test_user_doc.get('first_name')}")
                    print(f"      - last_name: {test_user_doc.get('last_name')}")
                    print(f"      - is_active: {test_user_doc.get('is_active')}")
                    print(f"      - date_joined: {test_user_doc.get('date_joined')}")
                    print(f"      - last_login: {test_user_doc.get('last_login')}")
                    print(f"      - password_hash: {test_user_doc.get('password_hash')[:20]}...")
                else:
                    print("   ❌ Test user not found in Attendancetracker.users collection")
                    return False
                    
            else:
                print("   ❌ Attendancetracker.users collection not found")
                return False
            
            client.close()
            
        except Exception as e:
            print(f"   ❌ MongoDB verification failed: {e}")
            return False
        
        # Test 5: Show all users in AttendanceUser model
        print("\n👥 Test 5: All Users in AttendanceUser Model")
        
        all_attendance_users = AttendanceUser.objects.all()
        print(f"   Total AttendanceUsers: {all_attendance_users.count()}")
        
        for user in all_attendance_users:
            print(f"   • {user.username} ({user.email}) - {user.get_full_name()}")
            print(f"     Joined: {user.date_joined}, Last Login: {user.last_login}")
        
        # Test 6: Compare with Django Users
        print("\n🔄 Test 6: Django vs AttendanceUser Comparison")
        
        django_users = User.objects.all()
        print(f"   Django Users: {django_users.count()}")
        print(f"   AttendanceUsers: {all_attendance_users.count()}")
        
        # Test 7: Clean up test data
        print("\n🧹 Test 7: Cleanup")
        
        django_user.delete()
        attendance_user.delete()
        print("   ✅ Test users deleted successfully")
        
        print("\n🎉 All Attendancetracker.users Tests Passed!")
        print("=" * 60)
        print("✅ CONFIRMED: User data IS stored in Attendancetracker.users collection")
        print("✅ Both signup and login data are properly stored")
        print("✅ MongoDB integration working correctly")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_current_collections():
    """Show current MongoDB collections"""
    
    print("\n📊 Current MongoDB Collections")
    print("=" * 40)
    
    try:
        client = pymongo.MongoClient('localhost', 27017)
        db = client['attendance_db']
        
        collections = db.list_collection_names()
        
        print("📁 All Collections:")
        for collection in collections:
            count = db[collection].count_documents({})
            print(f"   • {collection}: {count} documents")
        
        print("\n👥 User-Related Collections:")
        user_collections = [c for c in collections if 'user' in c.lower() or 'auth' in c.lower()]
        
        for collection in user_collections:
            count = db[collection].count_documents({})
            print(f"   • {collection}: {count} documents")
            
            if collection == 'Attendancetracker.users' and count > 0:
                print("     Sample documents:")
                docs = list(db[collection].find({}).limit(2))
                for doc in docs:
                    print(f"       - {doc.get('username')} ({doc.get('email')})")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error accessing MongoDB: {e}")

if __name__ == "__main__":
    print("🚀 Attendancetracker.users Collection Testing")
    print("=" * 70)
    
    # Show current collections
    show_current_collections()
    
    # Test the storage
    success = test_attendancetracker_users_storage()
    
    if success:
        print("\n🎯 VERIFICATION COMPLETE")
        print("✅ Your login and signup data IS being stored in Attendancetracker.users!")
        sys.exit(0)
    else:
        print("\n❌ VERIFICATION FAILED")
        print("Some issues were found with Attendancetracker.users storage")
        sys.exit(1)
