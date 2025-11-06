"""
Debug PDF Converter - Step by Step Testing
"""
import requests
import json
import os

def test_basic_pdf_upload():
    """Test basic PDF upload with detailed error info"""
    print("🔍 Testing basic PDF upload...")
    
    if not os.path.exists("pdfsam.pdf"):
        print("❌ PDF file not found")
        return False
    
    url = "http://localhost:8000/api/v1/pdf-to-json"
    
    with open("pdfsam.pdf", 'rb') as f:
        files = {'file': ('pdfsam.pdf', f, 'application/pdf')}
        data = {
            'model_name': 'azure/genailab-maas-gpt-4o',
            'extraction_type': 'general'
        }
        
        try:
            response = requests.post(url, files=files, data=data, timeout=30)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Success!")
                print(f"Pages: {result.get('page_count', 'N/A')}")
                print(f"Model: {result.get('model_used', 'N/A')}")
                return True
            else:
                print("❌ Failed")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False

def test_model_connection_detailed():
    """Test model connection with more details"""
    print("\n🔍 Testing model connection in detail...")
    
    url = "http://localhost:8000/api/v1/test-model"
    
    try:
        response = requests.post(url, params={"model_name": "azure/genailab-maas-gpt-4o"}, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                print("✅ Model connection working!")
                return True
            else:
                print("❌ Model connection failed")
                print(f"Error: {result.get('error', 'Unknown error')}")
                return False
        else:
            print("❌ HTTP error")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("🚀 PDF Converter Debug Tests")
    print("=" * 40)
    
    # Test model connection first
    model_ok = test_model_connection_detailed()
    
    # Test PDF upload
    pdf_ok = test_basic_pdf_upload()
    
    print("\n" + "=" * 40)
    print("📊 DEBUG RESULTS")
    print("=" * 40)
    print(f"Model Connection: {'✅ OK' if model_ok else '❌ FAILED'}")
    print(f"PDF Processing: {'✅ OK' if pdf_ok else '❌ FAILED'}")
