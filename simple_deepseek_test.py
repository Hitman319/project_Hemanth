"""
Simple DeepSeek Test - Direct Endpoint Test
"""
import requests
import json

def test_deepseek_direct():
    """Direct test of DeepSeek endpoint"""
    print("🎯 Direct DeepSeek Test")
    print("=" * 40)
    
    url = "http://localhost:8000/api/v1/generate-claim-json"
    
    payload = {
        "message": "John Anderson submitted a health insurance claim for hospitalization on October 15, 2024. Claim amount is $15,750.00 and has been approved.",
        "temperature": 0.1
    }
    
    print(f"Testing: {url}")
    print(f"Input: {payload['message'][:80]}...")
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Model: {result.get('model')}")
            print(f"Generated JSON:")
            print("-" * 40)
            print(result.get('generated_json', 'No JSON found'))
            print("-" * 40)
        else:
            print(f"❌ FAILED: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_deepseek_direct()
