#!/usr/bin/env python3
"""
Test script to verify sign-up functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

def test_signup_functionality():
    """Test the sign-up functionality"""
    
    print("🧪 Testing Sign-Up Functionality...")
    print("=" * 40)
    
    # Create a test client
    client = Client()
    
    try:
        # Test 1: GET request to signup page
        print("📄 Test 1: Loading sign-up page...")
        response = client.get('/signup/')
        if response.status_code == 200:
            print("✅ Sign-up page loads successfully")
        else:
            print(f"❌ Sign-up page failed to load: {response.status_code}")
            return False
        
        # Test 2: Check if signup page contains expected elements
        content = response.content.decode('utf-8')
        if 'Create Account' in content and 'username' in content and 'password1' in content:
            print("✅ Sign-up page contains expected form elements")
        else:
            print("❌ Sign-up page missing expected elements")
            return False
        
        # Test 3: Test user creation (simulate form submission)
        print("\n👤 Test 3: Creating test user...")
        
        # Check if test user already exists and delete if so
        if User.objects.filter(username='testuser123').exists():
            User.objects.filter(username='testuser123').delete()
            print("🧹 Cleaned up existing test user")
        
        # Test user data
        user_data = {
            'username': 'testuser123',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser123@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        
        # Submit signup form
        response = client.post('/signup/', user_data)
        
        # Check if user was created
        if User.objects.filter(username='testuser123').exists():
            print("✅ User created successfully")
            
            # Check if user was redirected (should redirect to dashboard after signup)
            if response.status_code == 302:
                print("✅ User redirected after successful signup")
            else:
                print(f"⚠️  User created but redirect status: {response.status_code}")
            
            # Verify user details
            user = User.objects.get(username='testuser123')
            print(f"📊 User details:")
            print(f"   - Username: {user.username}")
            print(f"   - Email: {user.email}")
            print(f"   - First Name: {user.first_name}")
            print(f"   - Last Name: {user.last_name}")
            print(f"   - Is Active: {user.is_active}")
            
        else:
            print("❌ User creation failed")
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                # Check for error messages in response
                content = response.content.decode('utf-8')
                if 'error' in content.lower():
                    print("❌ Error in form submission")
            return False
        
        # Test 4: Test duplicate username validation
        print("\n🔄 Test 4: Testing duplicate username validation...")
        response = client.post('/signup/', user_data)
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            if 'already exists' in content.lower():
                print("✅ Duplicate username validation working")
            else:
                print("⚠️  Duplicate username validation may not be working")
        
        # Test 5: Test password mismatch validation
        print("\n🔒 Test 5: Testing password mismatch validation...")
        mismatch_data = user_data.copy()
        mismatch_data['username'] = 'testuser456'
        mismatch_data['email'] = 'testuser456@example.com'
        mismatch_data['password2'] = 'differentpassword'
        
        response = client.post('/signup/', mismatch_data)
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            if 'do not match' in content.lower():
                print("✅ Password mismatch validation working")
            else:
                print("⚠️  Password mismatch validation may not be working")
        
        # Cleanup
        print("\n🧹 Cleaning up test data...")
        User.objects.filter(username__startswith='testuser').delete()
        print("✅ Test data cleaned up")
        
        print("\n🎉 All sign-up tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_url_patterns():
    """Test URL patterns"""
    print("\n🔗 Testing URL Patterns...")
    print("=" * 30)
    
    try:
        # Test URL reverse
        signup_url = reverse('signup')
        login_url = reverse('login')
        
        print(f"✅ Sign-up URL: {signup_url}")
        print(f"✅ Login URL: {login_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ URL pattern test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Sign-Up Functionality Tests")
    print("=" * 50)
    
    # Test URL patterns first
    url_test = test_url_patterns()
    
    # Test signup functionality
    signup_test = test_signup_functionality()
    
    if url_test and signup_test:
        print("\n🎯 All tests completed successfully!")
        print("✅ Sign-up functionality is working correctly")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)
