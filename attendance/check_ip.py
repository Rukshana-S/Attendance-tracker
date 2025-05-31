#!/usr/bin/env python3
"""
Check current public IP address for MongoDB Atlas whitelist
"""
import requests
import socket

def get_public_ip():
    """Get current public IP address"""
    try:
        # Try multiple services
        services = [
            'https://api.ipify.org',
            'https://ipinfo.io/ip',
            'https://httpbin.org/ip'
        ]
        
        for service in services:
            try:
                if 'httpbin' in service:
                    response = requests.get(service, timeout=5)
                    return response.json()['origin'].split(',')[0].strip()
                else:
                    response = requests.get(service, timeout=5)
                    return response.text.strip()
            except:
                continue
                
        return "Unable to determine"
        
    except Exception as e:
        return f"Error: {e}"

def get_local_ip():
    """Get local IP address"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Unable to determine"

if __name__ == "__main__":
    print("🌐 Network Information for MongoDB Atlas Setup")
    print("=" * 50)
    
    public_ip = get_public_ip()
    local_ip = get_local_ip()
    
    print(f"🌍 Public IP Address: {public_ip}")
    print(f"🏠 Local IP Address:  {local_ip}")
    print()
    print("📋 MongoDB Atlas Setup Instructions:")
    print("1. Go to MongoDB Atlas Dashboard")
    print("2. Navigate to 'Network Access' in the left sidebar")
    print("3. Click 'Add IP Address'")
    print(f"4. Add this IP address: {public_ip}")
    print("   OR")
    print("5. Add 0.0.0.0/0 to allow access from anywhere (for testing)")
    print()
    print("⚠️  Security Note:")
    print("   Using 0.0.0.0/0 allows access from any IP address.")
    print("   For production, use specific IP addresses only.")
