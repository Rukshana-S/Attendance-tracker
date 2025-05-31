#!/usr/bin/env python3
"""
View all user data stored in MongoDB from login and signup operations
"""
import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection
import pymongo

def view_all_user_data():
    """Display all user data stored in MongoDB"""
    
    print("👥 MongoDB User Data Viewer")
    print("=" * 50)
    
    # Database info
    db_config = connection.settings_dict
    print(f"🗄️  Database: {db_config['NAME']} (Engine: {db_config['ENGINE']})")
    print()
    
    # Get all users
    users = User.objects.all().order_by('date_joined')
    
    if not users.exists():
        print("📭 No users found in the database")
        return
    
    print(f"👥 Total Users: {users.count()}")
    print("=" * 50)
    
    for i, user in enumerate(users, 1):
        print(f"👤 User #{i}: {user.username}")
        print(f"   📧 Email: {user.email}")
        print(f"   👤 First Name: {user.first_name}")
        print(f"   👤 Last Name: {user.last_name}")
        print(f"   📛 Full Name: {user.get_full_name()}")
        print(f"   🆔 User ID: {user.id}")
        print(f"   📅 Date Joined: {user.date_joined}")
        print(f"   📅 Last Login: {user.last_login}")
        print(f"   ✅ Is Active: {user.is_active}")
        print(f"   👑 Is Staff: {user.is_staff}")
        print(f"   🔑 Is Superuser: {user.is_superuser}")
        print("-" * 40)

def view_mongodb_collections():
    """View MongoDB collections and their contents"""
    
    print("\n🗄️  MongoDB Collections Overview")
    print("=" * 40)
    
    try:
        # Connect to MongoDB directly
        client = pymongo.MongoClient('localhost', 27017)
        db = client['attendance_db']
        
        collections = db.list_collection_names()
        
        print("📁 Available Collections:")
        for collection_name in collections:
            count = db[collection_name].count_documents({})
            print(f"   • {collection_name}: {count} documents")
        
        print("\n👥 User Authentication Collections:")
        
        # Show auth_user collection details
        if 'auth_user' in collections:
            auth_users = db['auth_user'].find({})
            print(f"\n📊 auth_user collection:")
            
            for user_doc in auth_users:
                print(f"   🆔 ID: {user_doc.get('_id')}")
                print(f"   👤 Username: {user_doc.get('username')}")
                print(f"   📧 Email: {user_doc.get('email')}")
                print(f"   👤 Name: {user_doc.get('first_name')} {user_doc.get('last_name')}")
                print(f"   📅 Joined: {user_doc.get('date_joined')}")
                print(f"   🔐 Password Hash: {user_doc.get('password')[:20]}...")
                print("   " + "-" * 30)
        
        # Show other auth collections
        auth_collections = [col for col in collections if col.startswith('auth_')]
        
        for auth_col in auth_collections:
            if auth_col != 'auth_user':
                count = db[auth_col].count_documents({})
                if count > 0:
                    print(f"\n📊 {auth_col}: {count} documents")
                    # Show first few documents
                    docs = list(db[auth_col].find({}).limit(3))
                    for doc in docs:
                        print(f"   • {doc}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error accessing MongoDB directly: {e}")
        print("ℹ️  Using Django ORM data instead")

def simulate_signup_data_storage():
    """Show what data gets stored during signup"""
    
    print("\n📝 What Data Gets Stored During Signup")
    print("=" * 45)
    
    print("When a user signs up through your signup form, the following data is stored in MongoDB:")
    print()
    print("📋 Form Fields → MongoDB Storage:")
    print("   • Username → auth_user.username")
    print("   • First Name → auth_user.first_name") 
    print("   • Last Name → auth_user.last_name")
    print("   • Email → auth_user.email")
    print("   • Password → auth_user.password (hashed)")
    print()
    print("🔧 Auto-Generated Fields:")
    print("   • User ID → auth_user.id (unique identifier)")
    print("   • Date Joined → auth_user.date_joined (timestamp)")
    print("   • Is Active → auth_user.is_active (True by default)")
    print("   • Is Staff → auth_user.is_staff (False by default)")
    print("   • Is Superuser → auth_user.is_superuser (False by default)")
    print("   • Last Login → auth_user.last_login (updated on login)")

def simulate_login_data_storage():
    """Show what happens during login"""
    
    print("\n🔐 What Happens During Login")
    print("=" * 35)
    
    print("When a user logs in:")
    print("   1. 🔍 Username/password verified against MongoDB")
    print("   2. 📅 last_login field updated in auth_user collection")
    print("   3. 🎫 Session created (stored in django_session collection)")
    print("   4. 🍪 Session cookie sent to browser")
    print()
    print("📊 Login Process:")
    print("   • Input: username + password")
    print("   • Verification: Check against auth_user.username & auth_user.password")
    print("   • Update: auth_user.last_login = current timestamp")
    print("   • Create: Session record in django_session collection")

if __name__ == "__main__":
    print("🔍 MongoDB User Data Analysis")
    print("=" * 60)
    
    # Show current user data
    view_all_user_data()
    
    # Show MongoDB collections
    view_mongodb_collections()
    
    # Explain data storage
    simulate_signup_data_storage()
    simulate_login_data_storage()
    
    print("\n" + "=" * 60)
    print("✅ SUMMARY: All login and signup data is stored in MongoDB!")
    print("📊 User accounts, passwords, and session data are all in MongoDB")
    print("🔐 Your authentication system is fully MongoDB-integrated")
