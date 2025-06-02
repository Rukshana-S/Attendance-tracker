#!/usr/bin/env python3
"""
Test script to verify MongoDB Atlas connection
"""
import pymongo
from pymongo import MongoClient
import sys

def test_atlas_connection():
    """Test direct connection to MongoDB Atlas"""

    # Multiple connection string formats to try
    connection_strings = [
        "mongodb+srv://rukshanas2024cse:Oy4vyaw5cbj0i5UR@cluster0.vn91cjf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        "mongodb+srv://rukshanas2024cse:Oy4vyaw5cbj0i5UR@cluster0.vn91cjf.mongodb.net/attendance_db?retryWrites=true&w=majority",
        "mongodb+srv://rukshanas2024cse:Oy4vyaw5cbj0i5UR@cluster0.vn91cjf.mongodb.net/?retryWrites=true&w=majority"
    ]

    for i, connection_string in enumerate(connection_strings, 1):
        try:
            print(f"🔄 Testing MongoDB Atlas connection (attempt {i}/3)...")
            print(f"🔗 Connection string: {connection_string[:50]}...")

            # Create client with extended timeout
            client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=30000,
                connectTimeoutMS=30000,
                socketTimeoutMS=30000,
                maxPoolSize=1
            )

            # Test the connection
            print("📡 Attempting to connect...")
            result = client.admin.command('ping')
            print("✅ Successfully connected to MongoDB Atlas!")
            print(f"📊 Ping result: {result}")

            # Get database info
            db = client['attendance_db']
            print(f"📊 Database: {db.name}")

            # List collections
            collections = db.list_collection_names()
            print(f"📁 Collections: {collections}")

            # Test a simple operation
            test_collection = db['test_connection']
            test_doc = {"test": "connection", "timestamp": "2025-05-31", "attempt": i}
            result = test_collection.insert_one(test_doc)
            print(f"✅ Test document inserted with ID: {result.inserted_id}")

            # Clean up test document
            test_collection.delete_one({"_id": result.inserted_id})
            print("🧹 Test document cleaned up")

            # Close connection
            client.close()
            print("🔐 Connection closed successfully")

            return True

        except Exception as e:
            print(f"❌ Attempt {i} failed: {e}")
            if i < len(connection_strings):
                print("🔄 Trying next connection format...")
                continue
            else:
                print("💡 All connection attempts failed. This might be due to:")
                print("   - MongoDB Atlas cluster is paused or stopped")
                print("   - Network connectivity issues")
                print("   - Firewall blocking MongoDB ports")
                print("   - MongoDB Atlas IP whitelist restrictions")
                print("   - Incorrect credentials")
                return False

    return False

if __name__ == "__main__":
    success = test_atlas_connection()
    sys.exit(0 if success else 1)
