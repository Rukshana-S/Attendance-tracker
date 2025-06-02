#!/usr/bin/env python3
"""
Script to show all signup data stored in Attendancetracker.users collection
"""
import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
django.setup()

from myapp.models import AttendanceUser
from django.contrib.auth.models import User
import pymongo

def show_all_signup_data():
    """Show all signup data in Attendancetracker.users collection"""
    
    print("👥 ALL SIGNUP DATA IN ATTENDANCETRACKER.USERS")
    print("=" * 60)
    
    try:
        # Method 1: Using Django ORM
        print("📊 Method 1: Django ORM (AttendanceUser model)")
        print("-" * 50)
        
        attendance_users = AttendanceUser.objects.all().order_by('date_joined')
        
        if attendance_users.exists():
            print(f"✅ Found {attendance_users.count()} users in AttendanceUser model:")
            print()
            
            for i, user in enumerate(attendance_users, 1):
                print(f"👤 User #{i}: {user.username}")
                print(f"   📧 Email: {user.email}")
                print(f"   👤 First Name: {user.first_name}")
                print(f"   👤 Last Name: {user.last_name}")
                print(f"   📛 Full Name: {user.get_full_name()}")
                print(f"   🆔 User ID: {user.id}")
                print(f"   📅 Date Joined: {user.date_joined}")
                print(f"   📅 Last Login: {user.last_login}")
                print(f"   ✅ Is Active: {user.is_active}")
                print(f"   🔐 Password Hash: {user.password_hash[:30]}...")
                print("-" * 40)
        else:
            print("❌ No users found in AttendanceUser model")
        
        # Method 2: Direct MongoDB access
        print("\n🗄️  Method 2: Direct MongoDB Access")
        print("-" * 50)
        
        client = pymongo.MongoClient('localhost', 27017)
        db = client['attendance_db']
        
        # Check if collection exists
        collections = db.list_collection_names()
        
        if 'Attendancetracker.users' in collections:
            print("✅ Attendancetracker.users collection found in MongoDB")
            
            # Get all documents
            users_cursor = db['Attendancetracker.users'].find({}).sort("date_joined", 1)
            users_list = list(users_cursor)
            
            print(f"📊 Total documents in collection: {len(users_list)}")
            print()
            
            if users_list:
                for i, user_doc in enumerate(users_list, 1):
                    print(f"📄 Document #{i}:")
                    print(f"   🆔 MongoDB _id: {user_doc.get('_id')}")
                    print(f"   🆔 Django ID: {user_doc.get('id')}")
                    print(f"   👤 Username: {user_doc.get('username')}")
                    print(f"   📧 Email: {user_doc.get('email')}")
                    print(f"   👤 First Name: {user_doc.get('first_name')}")
                    print(f"   👤 Last Name: {user_doc.get('last_name')}")
                    print(f"   📅 Date Joined: {user_doc.get('date_joined')}")
                    print(f"   📅 Last Login: {user_doc.get('last_login')}")
                    print(f"   ✅ Is Active: {user_doc.get('is_active')}")
                    print(f"   🔐 Password Hash: {user_doc.get('password_hash', '')[:30]}...")
                    print("-" * 40)
            else:
                print("❌ No documents found in Attendancetracker.users collection")
        else:
            print("❌ Attendancetracker.users collection not found")
            print(f"📁 Available collections: {collections}")
        
        client.close()
        
        # Method 3: Compare with Django User model
        print("\n🔄 Method 3: Comparison with Django Users")
        print("-" * 50)
        
        django_users = User.objects.all().order_by('date_joined')
        
        print(f"📊 Django Users: {django_users.count()}")
        print(f"📊 AttendanceUsers: {attendance_users.count()}")
        print()
        
        print("📋 Django Users:")
        for user in django_users:
            print(f"   • {user.username} ({user.email}) - {user.get_full_name()}")
        
        print("\n📋 AttendanceUsers:")
        for user in attendance_users:
            print(f"   • {user.username} ({user.email}) - {user.get_full_name()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_new_signup():
    """Test creating a new signup to see the data flow"""
    
    print(f"\n🧪 TESTING NEW SIGNUP")
    print("=" * 30)
    
    test_username = f"test_signup_{datetime.now().strftime('%H%M%S')}"
    
    try:
        from django.test import Client
        
        # Test data
        signup_data = {
            'username': test_username,
            'first_name': 'Test',
            'last_name': 'Signup',
            'email': f'{test_username}@example.com',
            'password1': 'testsignup123',
            'password2': 'testsignup123'
        }
        
        print(f"📝 Creating new user: {test_username}")
        
        # Before counts
        before_django = User.objects.count()
        before_attendance = AttendanceUser.objects.count()
        
        print(f"📊 Before signup:")
        print(f"   Django Users: {before_django}")
        print(f"   AttendanceUsers: {before_attendance}")
        
        # Perform signup
        client = Client()
        response = client.post('/signup/', signup_data)
        
        print(f"📤 Signup response: {response.status_code}")
        
        # After counts
        after_django = User.objects.count()
        after_attendance = AttendanceUser.objects.count()
        
        print(f"📊 After signup:")
        print(f"   Django Users: {after_django} (+{after_django - before_django})")
        print(f"   AttendanceUsers: {after_attendance} (+{after_attendance - before_attendance})")
        
        # Check if user was created
        try:
            new_user = AttendanceUser.objects.get(username=test_username)
            print(f"✅ New user found in AttendanceUser: {new_user.username}")
            print(f"   📧 Email: {new_user.email}")
            print(f"   👤 Name: {new_user.get_full_name()}")
            
            # Check MongoDB
            client_mongo = pymongo.MongoClient('localhost', 27017)
            db = client_mongo['attendance_db']
            
            user_doc = db['Attendancetracker.users'].find_one({"username": test_username})
            if user_doc:
                print(f"✅ New user found in MongoDB: {user_doc['username']}")
            else:
                print(f"❌ New user not found in MongoDB")
            
            client_mongo.close()
            
            # Cleanup
            new_user.delete()
            User.objects.filter(username=test_username).delete()
            print(f"🧹 Test user cleaned up")
            
        except AttendanceUser.DoesNotExist:
            print(f"❌ New user not found in AttendanceUser model")
        
    except Exception as e:
        print(f"❌ Test signup failed: {e}")

def show_mongodb_connection_info():
    """Show MongoDB connection information"""
    
    print(f"\n🔗 MONGODB CONNECTION INFO")
    print("=" * 35)
    
    try:
        from django.db import connection
        db_config = connection.settings_dict
        
        print(f"🔧 Database Engine: {db_config['ENGINE']}")
        print(f"💾 Database Name: {db_config['NAME']}")
        
        if 'CLIENT' in db_config:
            client_config = db_config['CLIENT']
            host = client_config.get('host', 'localhost')
            port = client_config.get('port', 27017)
            print(f"🌐 Host: {host}")
            print(f"🔌 Port: {port}")
        
        # Test direct connection
        client = pymongo.MongoClient('localhost', 27017)
        db = client['attendance_db']
        
        collections = db.list_collection_names()
        print(f"📁 Total collections: {len(collections)}")
        
        if 'Attendancetracker.users' in collections:
            count = db['Attendancetracker.users'].count_documents({})
            print(f"👥 Users in Attendancetracker.users: {count}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Connection info error: {e}")

if __name__ == "__main__":
    print("🔍 SIGNUP DATA VIEWER")
    print("=" * 70)
    
    # Show connection info
    show_mongodb_connection_info()
    
    # Show all existing data
    show_all_signup_data()
    
    # Test new signup
    test_new_signup()
    
    print("\n🎯 SUMMARY")
    print("=" * 20)
    print("✅ If you see users listed above, your signup data IS being stored")
    print("✅ Check the 'Attendancetracker.users' collection in MongoDB")
    print("✅ You can also view users in Django Admin at /admin/")
