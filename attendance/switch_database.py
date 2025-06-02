#!/usr/bin/env python3
"""
Database Configuration Switcher
Switch between Local MongoDB and MongoDB Atlas
"""
import os
import sys

def set_environment_variable(key, value):
    """Set environment variable for current session"""
    os.environ[key] = value
    print(f"✅ Set {key}={value}")

def show_current_config():
    """Show current database configuration"""
    use_atlas = os.getenv('USE_ATLAS', 'false').lower() == 'true'
    
    print("🔍 Current Database Configuration:")
    print("=" * 40)
    
    if use_atlas:
        print("📡 Using: MongoDB Atlas (Cloud)")
        print("🌐 Host: cluster0.vn91cjf.mongodb.net")
        print("💾 Database: attendance_db")
        print("🔐 Authentication: SCRAM-SHA-1")
    else:
        print("🏠 Using: Local MongoDB")
        print("🌐 Host: localhost:27017")
        print("💾 Database: attendance_db")
        print("🔐 Authentication: None")
    
    print("=" * 40)

def switch_to_atlas():
    """Switch to MongoDB Atlas configuration"""
    print("🔄 Switching to MongoDB Atlas...")
    set_environment_variable('USE_ATLAS', 'true')
    print("📡 Now using MongoDB Atlas (Cloud)")
    print()
    print("⚠️  Important Notes:")
    print("   - Ensure your MongoDB Atlas cluster is running")
    print("   - Verify IP whitelist includes 0.0.0.0/0")
    print("   - Check network connectivity")
    print()
    print("🧪 Test the connection with:")
    print("   python manage.py test_mongodb")

def switch_to_local():
    """Switch to Local MongoDB configuration"""
    print("🔄 Switching to Local MongoDB...")
    set_environment_variable('USE_ATLAS', 'false')
    print("🏠 Now using Local MongoDB")
    print()
    print("⚠️  Important Notes:")
    print("   - Ensure MongoDB service is running locally")
    print("   - Default connection: localhost:27017")
    print()
    print("🧪 Test the connection with:")
    print("   python manage.py test_mongodb")

def test_current_connection():
    """Test current database connection"""
    print("🧪 Testing current database connection...")
    
    try:
        # Import Django settings
        import django
        from django.conf import settings
        
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
        django.setup()
        
        from django.db import connection
        from myapp.models import Student
        
        # Test connection
        students_count = Student.objects.count()
        print(f"✅ Connection successful!")
        print(f"📊 Students in database: {students_count}")
        
        # Show configuration
        db_config = connection.settings_dict
        print(f"🔧 Engine: {db_config['ENGINE']}")
        print(f"💾 Database: {db_config['NAME']}")
        
        if 'CLIENT' in db_config and 'host' in db_config['CLIENT']:
            host = db_config['CLIENT']['host']
            if 'mongodb+srv' in str(host):
                print("📡 Using: MongoDB Atlas")
            else:
                print("🏠 Using: Local MongoDB")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Try switching database configuration or check connection settings")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("🗄️  MongoDB Database Configuration Switcher")
        print("=" * 50)
        show_current_config()
        print()
        print("📋 Available Commands:")
        print("   python switch_database.py atlas    - Switch to MongoDB Atlas")
        print("   python switch_database.py local    - Switch to Local MongoDB")
        print("   python switch_database.py status   - Show current configuration")
        print("   python switch_database.py test     - Test current connection")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'atlas':
        switch_to_atlas()
    elif command == 'local':
        switch_to_local()
    elif command == 'status':
        show_current_config()
    elif command == 'test':
        test_current_connection()
    else:
        print(f"❌ Unknown command: {command}")
        print("📋 Available commands: atlas, local, status, test")

if __name__ == "__main__":
    main()
