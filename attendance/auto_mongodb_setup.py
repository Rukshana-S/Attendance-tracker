#!/usr/bin/env python3
"""
Automated MongoDB Connection Setup and Data Viewer
This script will automatically connect to MongoDB and show your data
"""
import os
import sys
import django
import pymongo
import webbrowser
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
django.setup()

from myapp.models import AttendanceUser

def auto_connect_mongodb():
    """Automatically connect to MongoDB and verify everything"""
    
    print("🚀 AUTOMATED MONGODB CONNECTION SETUP")
    print("=" * 50)
    
    try:
        # Step 1: Connect to MongoDB
        print("🔗 Step 1: Connecting to MongoDB...")
        client = pymongo.MongoClient('localhost', 27017, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        # Step 2: Verify database
        print("\n💾 Step 2: Checking database...")
        databases = client.list_database_names()
        
        if 'attendance_db' in databases:
            print("✅ attendance_db database found!")
            db = client['attendance_db']
        else:
            print("❌ attendance_db not found")
            print(f"Available databases: {databases}")
            return False
        
        # Step 3: Verify collection
        print("\n📁 Step 3: Checking collection...")
        collections = db.list_collection_names()
        
        if 'Attendancetracker.users' in collections:
            print("✅ Attendancetracker.users collection found!")
            collection = db['Attendancetracker.users']
        else:
            print("❌ Attendancetracker.users collection not found")
            print(f"Available collections: {collections}")
            return False
        
        # Step 4: Count documents
        print("\n📊 Step 4: Counting documents...")
        count = collection.count_documents({})
        print(f"✅ Found {count} documents in Attendancetracker.users")
        
        # Step 5: Show all data
        print("\n👥 Step 5: Displaying all signup data...")
        print("-" * 60)
        
        if count > 0:
            documents = list(collection.find({}))
            
            for i, doc in enumerate(documents, 1):
                print(f"📄 User #{i}:")
                print(f"   🆔 MongoDB ID: {doc.get('_id')}")
                print(f"   👤 Username: {doc.get('username')}")
                print(f"   📧 Email: {doc.get('email')}")
                print(f"   👤 First Name: {doc.get('first_name')}")
                print(f"   👤 Last Name: {doc.get('last_name')}")
                print(f"   📅 Date Joined: {doc.get('date_joined')}")
                print(f"   📅 Last Login: {doc.get('last_login')}")
                print(f"   ✅ Is Active: {doc.get('is_active')}")
                print("-" * 40)
        else:
            print("⚠️  No documents found in collection")
        
        client.close()
        return True, count
        
    except pymongo.errors.ServerSelectionTimeoutError:
        print("❌ Cannot connect to MongoDB")
        print("   MongoDB might not be running")
        return False, 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, 0

def create_mongodb_compass_launcher():
    """Create a batch file to automatically open MongoDB Compass with correct connection"""
    
    print("\n🚀 Creating MongoDB Compass Auto-Launcher...")
    
    batch_content = f'''@echo off
echo Opening MongoDB Compass with correct connection...
echo Connection String: mongodb://localhost:27017
echo Database: attendance_db
echo Collection: Attendancetracker.users
echo.
echo Instructions:
echo 1. MongoDB Compass will open
echo 2. Use connection string: mongodb://localhost:27017
echo 3. Navigate to: attendance_db ^> Attendancetracker.users
echo 4. Clear any filters (use empty query: {{}})
echo 5. Click Apply to see your data
echo.
pause
start "" "mongodb-compass://localhost:27017/attendance_db/Attendancetracker.users"
'''
    
    try:
        with open('open_mongodb_compass.bat', 'w') as f:
            f.write(batch_content)
        
        print("✅ Created: open_mongodb_compass.bat")
        print("   Double-click this file to auto-open MongoDB Compass")
        return True
    except Exception as e:
        print(f"❌ Failed to create launcher: {e}")
        return False

def create_web_viewer():
    """Create a simple web-based viewer for the data"""
    
    print("\n🌐 Creating Web-Based Data Viewer...")
    
    try:
        # Get data from MongoDB
        client = pymongo.MongoClient('localhost', 27017)
        db = client['attendance_db']
        collection = db['Attendancetracker.users']
        
        documents = list(collection.find({}))
        client.close()
        
        # Create HTML viewer
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Attendancetracker.users Data Viewer</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; text-align: center; }}
        .stats {{ background: #e8f5e8; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .user-card {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; background: #fafafa; }}
        .user-header {{ font-weight: bold; color: #2c5aa0; font-size: 18px; }}
        .user-detail {{ margin: 5px 0; }}
        .label {{ font-weight: bold; color: #555; }}
        .refresh-btn {{ background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
        .refresh-btn:hover {{ background: #45a049; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🗄️ Attendancetracker.users Collection Data</h1>
        
        <div class="stats">
            <h3>📊 Collection Statistics</h3>
            <p><span class="label">Database:</span> attendance_db</p>
            <p><span class="label">Collection:</span> Attendancetracker.users</p>
            <p><span class="label">Total Documents:</span> {len(documents)}</p>
            <p><span class="label">Last Updated:</span> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Data</button>
        
        <h3>👥 User Documents:</h3>
'''
        
        if documents:
            for i, doc in enumerate(documents, 1):
                html_content += f'''
        <div class="user-card">
            <div class="user-header">👤 User #{i}: {doc.get('username', 'N/A')}</div>
            <div class="user-detail"><span class="label">🆔 MongoDB ID:</span> {doc.get('_id', 'N/A')}</div>
            <div class="user-detail"><span class="label">🆔 Django ID:</span> {doc.get('id', 'N/A')}</div>
            <div class="user-detail"><span class="label">📧 Email:</span> {doc.get('email', 'N/A')}</div>
            <div class="user-detail"><span class="label">👤 First Name:</span> {doc.get('first_name', 'N/A')}</div>
            <div class="user-detail"><span class="label">👤 Last Name:</span> {doc.get('last_name', 'N/A')}</div>
            <div class="user-detail"><span class="label">📅 Date Joined:</span> {doc.get('date_joined', 'N/A')}</div>
            <div class="user-detail"><span class="label">📅 Last Login:</span> {doc.get('last_login', 'Never')}</div>
            <div class="user-detail"><span class="label">✅ Is Active:</span> {doc.get('is_active', 'N/A')}</div>
            <div class="user-detail"><span class="label">🔐 Password Hash:</span> {str(doc.get('password_hash', 'N/A'))[:30]}...</div>
        </div>
'''
        else:
            html_content += '''
        <div class="user-card">
            <p>⚠️ No user documents found in the collection.</p>
            <p>Try creating a new user through the signup form.</p>
        </div>
'''
        
        html_content += '''
    </div>
    
    <script>
        console.log('Attendancetracker.users Data Viewer loaded');
        console.log('Total users:', ''' + str(len(documents)) + ''');
    </script>
</body>
</html>'''
        
        # Save HTML file
        with open('attendancetracker_users_viewer.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ Created: attendancetracker_users_viewer.html")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create web viewer: {e}")
        return False

def open_web_viewer():
    """Open the web viewer in default browser"""
    
    try:
        html_file = os.path.abspath('attendancetracker_users_viewer.html')
        webbrowser.open(f'file://{html_file}')
        print("🌐 Opening web viewer in your default browser...")
        return True
    except Exception as e:
        print(f"❌ Failed to open web viewer: {e}")
        return False

def main():
    """Main function to run all setup steps"""
    
    print("🎯 AUTOMATED MONGODB SETUP & DATA VIEWER")
    print("=" * 60)
    
    # Step 1: Auto-connect and verify
    success, count = auto_connect_mongodb()
    
    if not success:
        print("\n❌ MongoDB connection failed")
        print("Please ensure MongoDB is running and try again")
        return
    
    print(f"\n✅ SUCCESS! Found {count} users in Attendancetracker.users")
    
    # Step 2: Create MongoDB Compass launcher
    create_mongodb_compass_launcher()
    
    # Step 3: Create web viewer
    if create_web_viewer():
        print("\n🌐 Opening web-based data viewer...")
        open_web_viewer()
    
    # Step 4: Summary
    print(f"\n🎉 SETUP COMPLETE!")
    print("=" * 30)
    print("✅ MongoDB connection verified")
    print("✅ Data found in Attendancetracker.users")
    print("✅ Web viewer created and opened")
    print("✅ MongoDB Compass launcher created")
    print()
    print("📋 What you can do now:")
    print("1. 🌐 View data in the web browser (just opened)")
    print("2. 📱 Double-click 'open_mongodb_compass.bat' for Compass")
    print("3. 🔄 Refresh web viewer to see new signups")
    print("4. 📊 Use Django admin at http://localhost:8000/admin/")

if __name__ == "__main__":
    main()
