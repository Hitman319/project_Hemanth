"""
Check what endpoints are available
"""
import requests
import json

try:
    response = requests.get("http://localhost:8000/openapi.json")
    if response.status_code == 200:
        openapi = response.json()
        print("📍 Available Endpoints:")
        for path, methods in openapi.get("paths", {}).items():
            for method in methods.keys():
                print(f"  {method.upper()} {path}")
    else:
        print(f"❌ Failed to get OpenAPI spec: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")
