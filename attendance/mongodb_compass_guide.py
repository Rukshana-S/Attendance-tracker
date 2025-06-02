#!/usr/bin/env python3
"""
MongoDB Compass Connection Guide and Data Verification
"""
import os
import sys
import django
import pymongo
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
django.setup()

from myapp.models import AttendanceUser

def verify_mongodb_connection():
    """Verify MongoDB connection and show connection details"""
    
    print("🔗 MONGODB COMPASS CONNECTION GUIDE")
    print("=" * 50)
    
    try:
        # Test MongoDB connection
        client = pymongo.MongoClient('localhost', 27017)
        
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB is running and accessible")
        
        # Show connection details
        print(f"\n📋 Connection Details:")
        print(f"   Host: localhost")
        print(f"   Port: 27017")
        print(f"   Connection String: mongodb://localhost:27017")
        
        # Show database info
        databases = client.list_database_names()
        print(f"\n💾 Available Databases:")
        for db_name in databases:
            if db_name in ['attendance_db', 'admin', 'config', 'local']:
                print(f"   • {db_name}")
        
        # Check attendance_db specifically
        if 'attendance_db' in databases:
            print(f"\n✅ attendance_db found!")
            
            db = client['attendance_db']
            collections = db.list_collection_names()
            
            print(f"📁 Collections in attendance_db:")
            for col in sorted(collections):
                count = db[col].count_documents({})
                if 'user' in col.lower() or 'attendance' in col.lower():
                    print(f"   • {col}: {count} documents ⭐")
                else:
                    print(f"   • {col}: {count} documents")
            
            # Check Attendancetracker.users specifically
            if 'Attendancetracker.users' in collections:
                print(f"\n🎯 Attendancetracker.users Collection:")
                
                collection = db['Attendancetracker.users']
                count = collection.count_documents({})
                print(f"   📊 Total Documents: {count}")
                
                if count > 0:
                    print(f"   📄 Sample Documents:")
                    for i, doc in enumerate(collection.find().limit(3), 1):
                        print(f"      {i}. {doc.get('username')} ({doc.get('email')})")
                        print(f"         Name: {doc.get('first_name')} {doc.get('last_name')}")
                        print(f"         Joined: {doc.get('date_joined')}")
                        print()
                else:
                    print(f"   ⚠️  No documents found")
            else:
                print(f"\n❌ Attendancetracker.users collection not found")
        else:
            print(f"\n❌ attendance_db database not found")
        
        client.close()
        return True
        
    except pymongo.errors.ServerSelectionTimeoutError:
        print("❌ Cannot connect to MongoDB")
        print("   Make sure MongoDB is running on localhost:27017")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_compass_instructions():
    """Show step-by-step MongoDB Compass instructions"""
    
    print(f"\n📱 MONGODB COMPASS SETUP INSTRUCTIONS")
    print("=" * 45)
    
    print(f"1. 📥 Download MongoDB Compass:")
    print(f"   https://www.mongodb.com/try/download/compass")
    print()
    
    print(f"2. 🔗 Connection String:")
    print(f"   mongodb://localhost:27017")
    print()
    
    print(f"3. 📂 Navigate to Your Data:")
    print(f"   Database: attendance_db")
    print(f"   Collection: Attendancetracker.users")
    print()
    
    print(f"4. 🔍 View Your Signup Data:")
    print(f"   - Clear any filters (use empty query: {{}})")
    print(f"   - Click 'Apply' or 'Find'")
    print(f"   - You should see your user documents")
    print()
    
    print(f"5. 🎯 Expected Data:")
    
    # Show current users
    try:
        users = AttendanceUser.objects.all()
        if users.exists():
            print(f"   You should see {users.count()} user(s):")
            for user in users:
                print(f"   • {user.username} ({user.email})")
        else:
            print(f"   No users found in Django ORM")
    except Exception as e:
        print(f"   Error checking users: {e}")

def create_test_document():
    """Create a test document to verify Compass can see new data"""
    
    print(f"\n🧪 CREATING TEST DOCUMENT")
    print("=" * 30)
    
    try:
        from django.contrib.auth.hashers import make_password
        from django.utils import timezone
        
        # Create test user
        test_username = f"compass_test_{datetime.now().strftime('%H%M%S')}"
        
        test_user = AttendanceUser.objects.create(
            username=test_username,
            email=f"{test_username}@compass.test",
            first_name="Compass",
            last_name="Test",
            password_hash=make_password("testpass123"),
            is_active=True,
            date_joined=timezone.now()
        )
        
        print(f"✅ Test user created: {test_user.username}")
        print(f"📧 Email: {test_user.email}")
        print(f"🆔 ID: {test_user.id}")
        
        # Verify in MongoDB
        client = pymongo.MongoClient('localhost', 27017)
        db = client['attendance_db']
        
        doc = db['Attendancetracker.users'].find_one({"username": test_username})
        if doc:
            print(f"✅ Test user found in MongoDB")
            print(f"📄 MongoDB _id: {doc['_id']}")
        else:
            print(f"❌ Test user not found in MongoDB")
        
        client.close()
        
        print(f"\n🔍 Now check MongoDB Compass:")
        print(f"   1. Refresh the Attendancetracker.users collection")
        print(f"   2. Look for user: {test_username}")
        print(f"   3. If you see it, Compass is working correctly!")
        
        # Cleanup after 10 seconds
        import time
        print(f"\n⏰ Test user will be deleted in 10 seconds...")
        time.sleep(10)
        
        test_user.delete()
        print(f"🧹 Test user deleted")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def troubleshoot_compass():
    """Troubleshooting guide for common Compass issues"""
    
    print(f"\n🔧 TROUBLESHOOTING MONGODB COMPASS")
    print("=" * 40)
    
    print(f"❓ Problem: Can't see documents in Attendancetracker.users")
    print(f"✅ Solutions:")
    print(f"   1. Clear filter: Use empty query {{}}")
    print(f"   2. Refresh: Click the refresh button")
    print(f"   3. Check connection: Ensure connected to localhost:27017")
    print(f"   4. Check database: Make sure you're in 'attendance_db'")
    print(f"   5. Check collection: Make sure you're in 'Attendancetracker.users'")
    print()
    
    print(f"❓ Problem: Connection failed")
    print(f"✅ Solutions:")
    print(f"   1. Check MongoDB is running: Run 'mongosh' in command prompt")
    print(f"   2. Use correct connection string: mongodb://localhost:27017")
    print(f"   3. No authentication needed for local MongoDB")
    print()
    
    print(f"❓ Problem: Database/Collection not found")
    print(f"✅ Solutions:")
    print(f"   1. Run Django migrations: python manage.py migrate")
    print(f"   2. Create test user: Use signup form")
    print(f"   3. Check database name: Should be 'attendance_db'")

if __name__ == "__main__":
    print("🚀 MongoDB Compass Connection Helper")
    print("=" * 60)
    
    # Verify MongoDB connection
    if verify_mongodb_connection():
        print("\n" + "="*60)
        
        # Show Compass instructions
        show_compass_instructions()
        
        # Ask if user wants to create test document
        print(f"\n🧪 Would you like to create a test document to verify Compass?")
        print(f"This will help confirm that Compass can see new data.")
        
        response = input("Create test document? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            create_test_document()
        
        # Show troubleshooting
        troubleshoot_compass()
        
        print(f"\n🎯 SUMMARY")
        print(f"✅ MongoDB is running and accessible")
        print(f"✅ Your data is stored in: attendance_db.Attendancetracker.users")
        print(f"✅ Use connection string: mongodb://localhost:27017")
        print(f"✅ Navigate to: attendance_db → Attendancetracker.users")
        
    else:
        print(f"\n❌ MongoDB connection failed")
        print(f"Please start MongoDB service and try again")
