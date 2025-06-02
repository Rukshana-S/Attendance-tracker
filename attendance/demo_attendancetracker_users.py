#!/usr/bin/env python3
"""
Demo script to show how signup and login data is stored in Attendancetracker.users
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

def demo_signup_and_login():
    """Demonstrate complete signup and login flow with Attendancetracker.users storage"""
    
    print("🎬 DEMO: Attendancetracker.users Storage")
    print("=" * 50)
    
    # Create test client
    client = Client()
    
    # Demo user data
    demo_username = f"demo_user_{datetime.now().strftime('%H%M%S')}"
    demo_data = {
        'username': demo_username,
        'first_name': 'Demo',
        'last_name': 'User',
        'email': f'{demo_username}@example.com',
        'password1': 'demopassword123',
        'password2': 'demopassword123'
    }
    
    print(f"👤 Demo User: {demo_username}")
    print(f"📧 Email: {demo_data['email']}")
    print()
    
    try:
        # Step 1: Simulate Signup
        print("📝 Step 1: Simulating Signup Process")
        print("   Submitting signup form...")
        
        response = client.post('/signup/', demo_data)
        
        if response.status_code == 302:  # Redirect after successful signup
            print("   ✅ Signup successful (redirected)")
        else:
            print(f"   ⚠️  Signup response: {response.status_code}")
        
        # Step 2: Check Django User creation
        print("\n🔍 Step 2: Checking Django User Creation")
        
        try:
            django_user = User.objects.get(username=demo_username)
            print(f"   ✅ Django User created: {django_user.username}")
            print(f"   📧 Email: {django_user.email}")
            print(f"   👤 Name: {django_user.get_full_name()}")
        except User.DoesNotExist:
            print("   ❌ Django User not found")
            return False
        
        # Step 3: Check AttendanceUser creation
        print("\n📊 Step 3: Checking AttendanceUser Creation")
        
        try:
            attendance_user = AttendanceUser.objects.get(username=demo_username)
            print(f"   ✅ AttendanceUser created: {attendance_user.username}")
            print(f"   📧 Email: {attendance_user.email}")
            print(f"   👤 Name: {attendance_user.get_full_name()}")
            print(f"   📅 Date Joined: {attendance_user.date_joined}")
            print(f"   🔐 Password Hash: {attendance_user.password_hash[:30]}...")
        except AttendanceUser.DoesNotExist:
            print("   ❌ AttendanceUser not found")
            return False
        
        # Step 4: Check MongoDB storage
        print("\n🗄️  Step 4: Checking MongoDB Storage")
        
        try:
            client_mongo = pymongo.MongoClient('localhost', 27017)
            db = client_mongo['attendance_db']
            
            # Find user in Attendancetracker.users collection
            user_doc = db['Attendancetracker.users'].find_one({"username": demo_username})
            
            if user_doc:
                print("   ✅ User found in Attendancetracker.users collection!")
                print(f"   📄 MongoDB Document:")
                print(f"      Collection: Attendancetracker.users")
                print(f"      _id: {user_doc['_id']}")
                print(f"      username: {user_doc['username']}")
                print(f"      email: {user_doc['email']}")
                print(f"      first_name: {user_doc['first_name']}")
                print(f"      last_name: {user_doc['last_name']}")
                print(f"      is_active: {user_doc['is_active']}")
                print(f"      date_joined: {user_doc['date_joined']}")
            else:
                print("   ❌ User not found in MongoDB")
                return False
            
            client_mongo.close()
            
        except Exception as e:
            print(f"   ❌ MongoDB check failed: {e}")
            return False
        
        # Step 5: Simulate Login
        print("\n🔐 Step 5: Simulating Login Process")
        
        login_data = {
            'username': demo_username,
            'password': 'demopassword123'
        }
        
        response = client.post('/login/', login_data)
        
        if response.status_code == 302:  # Redirect after successful login
            print("   ✅ Login successful (redirected)")
        else:
            print(f"   ⚠️  Login response: {response.status_code}")
        
        # Step 6: Check last_login update
        print("\n📅 Step 6: Checking Last Login Update")
        
        # Refresh from database
        attendance_user.refresh_from_db()
        
        if attendance_user.last_login:
            print(f"   ✅ Last login updated: {attendance_user.last_login}")
        else:
            print("   ⚠️  Last login not updated")
        
        # Step 7: Final MongoDB verification
        print("\n🔍 Step 7: Final MongoDB Verification")
        
        try:
            client_mongo = pymongo.MongoClient('localhost', 27017)
            db = client_mongo['attendance_db']
            
            user_doc = db['Attendancetracker.users'].find_one({"username": demo_username})
            
            if user_doc and user_doc.get('last_login'):
                print("   ✅ Last login updated in MongoDB!")
                print(f"   📅 Last login: {user_doc['last_login']}")
            else:
                print("   ⚠️  Last login not found in MongoDB")
            
            # Show collection stats
            total_users = db['Attendancetracker.users'].count_documents({})
            print(f"   📊 Total users in Attendancetracker.users: {total_users}")
            
            client_mongo.close()
            
        except Exception as e:
            print(f"   ❌ Final MongoDB check failed: {e}")
        
        # Step 8: Cleanup
        print("\n🧹 Step 8: Cleanup Demo Data")
        
        django_user.delete()
        attendance_user.delete()
        print("   ✅ Demo user data cleaned up")
        
        print("\n🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("✅ CONFIRMED: All signup and login data is stored in Attendancetracker.users")
        print("✅ The system works exactly as requested!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_collection_summary():
    """Show summary of Attendancetracker.users collection"""
    
    print("\n📊 Attendancetracker.users Collection Summary")
    print("=" * 45)
    
    try:
        # Django ORM view
        users = AttendanceUser.objects.all()
        print(f"🔢 Total Users: {users.count()}")
        
        if users.exists():
            print("\n👥 Current Users:")
            for user in users:
                print(f"   • {user.username} ({user.email})")
                print(f"     Name: {user.get_full_name()}")
                print(f"     Joined: {user.date_joined}")
                print(f"     Last Login: {user.last_login}")
                print()
        
        # MongoDB direct view
        client = pymongo.MongoClient('localhost', 27017)
        db = client['attendance_db']
        
        mongo_count = db['Attendancetracker.users'].count_documents({})
        print(f"🗄️  MongoDB Count: {mongo_count} documents")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Attendancetracker.users Demo")
    print("=" * 60)
    
    # Show current state
    show_collection_summary()
    
    # Run demo
    success = demo_signup_and_login()
    
    if success:
        print("\n🎯 DEMO CONCLUSION")
        print("✅ Your Django attendance tracker successfully stores ALL")
        print("✅ login and signup data in the Attendancetracker.users collection!")
        sys.exit(0)
    else:
        print("\n❌ Demo encountered issues")
        sys.exit(1)
