# MongoDB Atlas Setup Guide for Django Attendance Tracker

## 🎯 Current Status: Configuring MongoDB Atlas Connection

Your Django project is being configured to connect to MongoDB Atlas cloud database.

## 📋 Prerequisites Completed

✅ **Dependencies Installed**:
- `djongo==1.3.7` - Django-MongoDB connector
- `pymongo==3.11.4` - MongoDB Python driver  
- `dnspython==2.7.0` - Required for MongoDB Atlas SRV records

## 🔧 Current Configuration

### Database Settings
```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'attendance_db',
        'CLIENT': {
            'host': 'mongodb+srv://rukshanas2024cse:Oy4vyaw5cbj0i5UR@cluster0.vn91cjf.mongodb.net/attendance_db?retryWrites=true&w=majority',
            'authSource': 'admin',
            'authMechanism': 'SCRAM-SHA-1',
            'serverSelectionTimeoutMS': 30000,
            'connectTimeoutMS': 30000,
            'socketTimeoutMS': 30000,
        }
    }
}
```

## 🌐 Network Configuration Required

**Your Current IP Address**: `121.200.55.210`

### MongoDB Atlas IP Whitelist Setup

1. **Login to MongoDB Atlas**:
   - Go to [MongoDB Atlas](https://cloud.mongodb.com/)
   - Login with your credentials

2. **Navigate to Network Access**:
   - Click on "Network Access" in the left sidebar
   - Click "Add IP Address"

3. **Add Your IP Address**:
   - **Option A (Recommended for Production)**: Add `121.200.55.210`
   - **Option B (For Testing)**: Add `0.0.0.0/0` (allows access from anywhere)

4. **Save Changes**:
   - Click "Confirm" to save the IP whitelist entry
   - Wait for the changes to propagate (usually 1-2 minutes)

## 🔍 Connection Testing

### Test 1: Direct PyMongo Connection
```bash
python test_atlas_connection.py
```

### Test 2: Django-MongoDB Integration
```bash
python manage.py test_mongodb
```

### Test 3: Django System Check
```bash
python manage.py check
```

## 🚨 Troubleshooting Common Issues

### Issue 1: Connection Timeout
**Error**: `ServerSelectionTimeoutError`
**Solutions**:
1. Check IP whitelist in MongoDB Atlas
2. Verify internet connection
3. Check firewall settings
4. Ensure MongoDB Atlas cluster is running

### Issue 2: Authentication Failed
**Error**: `OperationFailure: Authentication failed`
**Solutions**:
1. Verify username and password in connection string
2. Check database user permissions in MongoDB Atlas
3. Ensure user has read/write access to the database

### Issue 3: DNS Resolution Issues
**Error**: DNS-related errors
**Solutions**:
1. Ensure `dnspython` is installed
2. Check internet connectivity
3. Try using direct connection string instead of SRV

## 🔄 Alternative Configuration Methods

### Method 1: Environment Variables (Recommended for Production)
Create a `.env` file:
```env
MONGODB_URI=mongodb+srv://rukshanas2024cse:Oy4vyaw5cbj0i5UR@cluster0.vn91cjf.mongodb.net/attendance_db?retryWrites=true&w=majority
```

Update settings.py:
```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'attendance_db',
        'CLIENT': {
            'host': os.getenv('MONGODB_URI'),
            'authSource': 'admin',
        }
    }
}
```

### Method 2: Direct Connection String
```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'attendance_db',
        'CLIENT': {
            'host': 'mongodb+srv://rukshanas2024cse:Oy4vyaw5cbj0i5UR@cluster0.vn91cjf.mongodb.net',
            'authSource': 'admin',
        }
    }
}
```

## 📊 Data Migration

Once connected, you may need to migrate your existing data:

### Option 1: Fresh Start (Recommended)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Option 2: Export/Import Data
```bash
# Export from local MongoDB
mongodump --db attendance_db --out backup/

# Import to Atlas (requires mongorestore with Atlas connection)
mongorestore --uri "mongodb+srv://..." backup/attendance_db/
```

## ✅ Verification Steps

1. **IP Whitelist**: Ensure your IP (121.200.55.210) is added to MongoDB Atlas
2. **Connection Test**: Run `python test_atlas_connection.py`
3. **Django Test**: Run `python manage.py test_mongodb`
4. **Application Test**: Run `python manage.py runserver`

## 🔐 Security Best Practices

1. **Use Environment Variables**: Store connection strings in environment variables
2. **Restrict IP Access**: Only whitelist necessary IP addresses
3. **Database User Permissions**: Create users with minimal required permissions
4. **Regular Password Updates**: Change database passwords regularly
5. **Enable Audit Logs**: Monitor database access in MongoDB Atlas

## 📞 Support

If you continue to experience connection issues:

1. **Check MongoDB Atlas Status**: [MongoDB Status Page](https://status.mongodb.com/)
2. **Review Atlas Documentation**: [MongoDB Atlas Docs](https://docs.atlas.mongodb.com/)
3. **Contact Support**: MongoDB Atlas support for connection issues

## 🎯 Next Steps

1. **Complete IP Whitelist Setup** in MongoDB Atlas
2. **Test Connection** using provided scripts
3. **Run Django Migrations** to create collections
4. **Test Application** functionality
5. **Deploy to Production** with proper security measures
