@echo off
echo Opening MongoDB Compass with correct connection...
echo Connection String: mongodb://localhost:27017
echo Database: attendance_db
echo Collection: Attendancetracker.users
echo.
echo Instructions:
echo 1. MongoDB Compass will open
echo 2. Use connection string: mongodb://localhost:27017
echo 3. Navigate to: attendance_db ^> Attendancetracker.users
echo 4. Clear any filters (use empty query: {})
echo 5. Click Apply to see your data
echo.
pause
start "" "mongodb-compass://localhost:27017/attendance_db/Attendancetracker.users"
