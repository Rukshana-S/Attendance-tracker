# MongoDB Atlas Connection Troubleshooting Guide

## 🚨 Current Issue: Connection Timeout (WinError 10060)

Your Django project is configured for MongoDB Atlas, but the connection is failing with a network timeout error.

## 🔍 Diagnosis

**Error**: `WinError 10060 - Connection attempt failed`
**Meaning**: The connection request is timing out, indicating network-level issues.

## 🛠️ Step-by-Step Solutions

### Solution 1: Check MongoDB Atlas Cluster Status

1. **Login to MongoDB Atlas**: https://cloud.mongodb.com/
2. **Navigate to your cluster**: Look for "Cluster0"
3. **Check cluster status**:
   - ✅ **Running**: Green indicator, shows "Active"
   - ❌ **Paused**: Yellow/Red indicator, shows "Paused"
   - ❌ **Stopped**: Red indicator, shows "Stopped"

4. **If paused/stopped**: Click "Resume" or "Start" button

### Solution 2: Verify IP Whitelist Configuration

1. **Go to Network Access** in MongoDB Atlas
2. **Check IP Address entries**:
   - Should see `0.0.0.0/0` (allows all IPs)
   - OR your specific IP address
3. **If missing**: Click "Add IP Address" → Enter `0.0.0.0/0` → Confirm
4. **Wait 2-3 minutes** for changes to propagate

### Solution 3: Verify Database User Credentials

1. **Go to Database Access** in MongoDB Atlas
2. **Check user**: `rukshanas2024cse`
3. **Verify**:
   - User exists and is enabled
   - Password is correct: `Oy4vyaw5cbj0i5UR`
   - User has read/write permissions
   - Authentication database is set to "admin"

### Solution 4: Test Network Connectivity

Run these commands to test basic connectivity:

```bash
# Test DNS resolution
nslookup cluster0.vn91cjf.mongodb.net

# Test basic connectivity (if available)
telnet cluster0.vn91cjf.mongodb.net 27017
```

### Solution 5: Check Windows Firewall

1. **Open Windows Defender Firewall**
2. **Check if MongoDB ports are blocked**:
   - Port 27017 (MongoDB default)
   - Port 27016-27019 (MongoDB range)
3. **Temporarily disable firewall** to test (re-enable after testing)

## 🔄 Alternative Configuration Options

### Option A: Hybrid Configuration (Recommended)

Use local MongoDB as fallback while troubleshooting Atlas:

```python
# In settings.py
import os

# Try Atlas first, fallback to local
MONGODB_ATLAS_URI = "mongodb+srv://rukshanas2024cse:Oy4vyaw5cbj0i5UR@cluster0.vn91cjf.mongodb.net/attendance_db?retryWrites=true&w=majority"
MONGODB_LOCAL_URI = "mongodb://localhost:27017"

# Use environment variable to switch
USE_ATLAS = os.getenv('USE_ATLAS', 'false').lower() == 'true'

if USE_ATLAS:
    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': 'attendance_db',
            'CLIENT': {
                'host': MONGODB_ATLAS_URI,
                'authSource': 'admin',
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': 'attendance_db',
            'CLIENT': {
                'host': 'localhost',
                'port': 27017,
            }
        }
    }
```

### Option B: Environment-Based Configuration

Create `.env` file:
```env
MONGODB_URI=mongodb+srv://rukshanas2024cse:Oy4vyaw5cbj0i5UR@cluster0.vn91cjf.mongodb.net/attendance_db?retryWrites=true&w=majority
USE_ATLAS=true
```

## 🧪 Testing Steps

### Test 1: Basic Network Test
```bash
ping cluster0.vn91cjf.mongodb.net
```

### Test 2: MongoDB Atlas Dashboard
- Login and verify cluster is running
- Check recent activity logs

### Test 3: Alternative Connection String
Try this simplified connection string:
```
mongodb+srv://rukshanas2024cse:Oy4vyaw5cbj0i5UR@cluster0.vn91cjf.mongodb.net/test
```

### Test 4: MongoDB Compass (GUI Tool)
1. Download MongoDB Compass
2. Use the connection string to test connectivity
3. If Compass connects, the issue is with Python/Django configuration

## 🔧 Quick Fixes to Try

### Fix 1: Update Connection String Format
```python
# Try this format in settings.py
'host': 'mongodb+srv://rukshanas2024cse:Oy4vyaw5cbj0i5UR@cluster0.vn91cjf.mongodb.net/attendance_db?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE'
```

### Fix 2: Add SSL Configuration
```python
'CLIENT': {
    'host': 'mongodb+srv://rukshanas2024cse:Oy4vyaw5cbj0i5UR@cluster0.vn91cjf.mongodb.net/attendance_db?retryWrites=true&w=majority',
    'authSource': 'admin',
    'ssl': True,
    'ssl_cert_reqs': 'CERT_NONE'
}
```

### Fix 3: Increase Timeouts
```python
'CLIENT': {
    'host': 'mongodb+srv://rukshanas2024cse:Oy4vyaw5cbj0i5UR@cluster0.vn91cjf.mongodb.net/attendance_db?retryWrites=true&w=majority',
    'authSource': 'admin',
    'serverSelectionTimeoutMS': 60000,
    'connectTimeoutMS': 60000,
    'socketTimeoutMS': 60000,
}
```

## 📞 Next Steps

1. **Check Atlas Dashboard** - Verify cluster is running
2. **Verify IP Whitelist** - Ensure 0.0.0.0/0 is added
3. **Test with MongoDB Compass** - Verify connection works outside Django
4. **Try alternative connection strings** - Test different formats
5. **Contact MongoDB Support** - If all else fails

## 🎯 Immediate Action Plan

**Right Now**:
1. Login to MongoDB Atlas
2. Check if cluster is paused → Resume if needed
3. Verify IP whitelist has 0.0.0.0/0
4. Wait 2-3 minutes and test again

**If Still Failing**:
1. Use local MongoDB temporarily
2. Download MongoDB Compass to test connection
3. Check Windows Firewall settings
4. Contact MongoDB Atlas support

Your Django configuration is correct - the issue is network/Atlas configuration related!
