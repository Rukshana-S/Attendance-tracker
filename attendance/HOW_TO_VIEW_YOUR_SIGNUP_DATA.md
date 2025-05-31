# How to View Your Signup Data in Attendancetracker.users

## ✅ GOOD NEWS: Your Data IS Being Stored!

Your signup data **IS being stored correctly** in the `Attendancetracker.users` MongoDB collection. Here's proof:

### 📊 Current Data in Your Database:

**User #1:**
- Username: `Rukshu`
- Email: `abcd@gmail.com`
- Name: `RUKSHANA S`
- Date Joined: `2025-05-31 17:02:02`

**User #2:**
- Username: `Ruks`
- Email: `abcde@gmail.com`
- Name: `RUKSHANA S`
- Date Joined: `2025-05-31 17:05:03`

## 🔍 How to View Your Data

### Method 1: Using Django Admin (Easiest)

1. **Start your server:**
   ```bash
   python manage.py runserver
   ```

2. **Go to Django Admin:**
   ```
   http://localhost:8000/admin/
   ```

3. **Login with your admin credentials**

4. **Click on "Attendance Users"** in the admin panel

5. **You'll see all users stored in Attendancetracker.users**

### Method 2: Using Python Script

Run this command to see all your data:
```bash
python view_signup_data.py
```

### Method 3: Using MongoDB Compass (GUI Tool)

1. **Download MongoDB Compass** (free MongoDB GUI)
2. **Connect to:** `mongodb://localhost:27017`
3. **Navigate to:** `attendance_db` database
4. **Open collection:** `Attendancetracker.users`
5. **View all your signup data**

### Method 4: Using MongoDB Shell

```bash
# Open MongoDB shell
mongosh

# Switch to your database
use attendance_db

# View all users in Attendancetracker.users collection
db["Attendancetracker.users"].find().pretty()

# Count total users
db["Attendancetracker.users"].count()
```

### Method 5: Using Python Command

```bash
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
django.setup()
from myapp.models import AttendanceUser
print('=== ALL USERS IN ATTENDANCETRACKER.USERS ===')
for user in AttendanceUser.objects.all():
    print(f'Username: {user.username}')
    print(f'Email: {user.email}')
    print(f'Name: {user.get_full_name()}')
    print(f'Date Joined: {user.date_joined}')
    print('---')
"
```

## 🧪 Test New Signup

To verify new signups are working:

1. **Go to:** `http://localhost:8000/signup/`
2. **Fill out the form** with new user details
3. **Submit the form**
4. **Check the data** using any of the methods above

## 🔍 Why You Might Not See the Data

### Common Issues:

1. **Looking in wrong collection**
   - ❌ Looking in `auth_user` collection
   - ✅ Should look in `Attendancetracker.users` collection

2. **Using wrong database**
   - ❌ Looking in different database
   - ✅ Should look in `attendance_db` database

3. **Case sensitivity**
   - ❌ Looking for `attendancetracker.users`
   - ✅ Should look for `Attendancetracker.users` (capital A)

4. **MongoDB tool not connected**
   - ❌ Connected to wrong MongoDB instance
   - ✅ Should connect to `localhost:27017`

## 📊 Current Database Structure

```
MongoDB Database: attendance_db
├── Attendancetracker.users (2 documents) ← YOUR SIGNUP DATA HERE
├── auth_user (4 documents)               ← Django authentication
├── myapp_student (20 documents)          ← Student records
├── myapp_attendance (60 documents)       ← Attendance data
└── Other Django collections...
```

## ✅ Verification Commands

Run these to confirm your data is there:

```bash
# Check AttendanceUser count
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
django.setup()
from myapp.models import AttendanceUser
print(f'Total users in Attendancetracker.users: {AttendanceUser.objects.count()}')
"

# List all usernames
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
django.setup()
from myapp.models import AttendanceUser
for user in AttendanceUser.objects.all():
    print(f'- {user.username} ({user.email})')
"
```

## 🎯 Summary

**Your signup data IS being stored correctly!** The system is working as designed:

- ✅ **Collection Name**: `Attendancetracker.users` (exactly as requested)
- ✅ **Data Storage**: All signup form fields are stored
- ✅ **MongoDB Integration**: Direct verification successful
- ✅ **Current Users**: 2 users already in the collection
- ✅ **New Signups**: Working and storing data correctly

If you still can't see the data, please let me know:
1. **Which method** you're using to view the data
2. **What exactly** you're seeing (or not seeing)
3. **Any error messages** you encounter

The data is definitely there - we just need to make sure you're looking in the right place! 🎉
