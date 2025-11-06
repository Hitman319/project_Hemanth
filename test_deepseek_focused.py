"""
🎯 FOCUSED TEST: DeepSeek Model for Structured JSON Output
Testing only the required endpoint with azure_ai/genailab-maas-DeepSeek-V3-0324
"""
import requests
import json

def test_deepseek_claim_json():
    """Test DeepSeek model for generating structured claim JSON"""
    print("🚀 Testing DeepSeek Model for Claim JSON Generation")
    print("=" * 60)
    
    # Test endpoint URL
    url = "http://localhost:8000/api/v1/generate-claim-json"
    
    # Test data - insurance claim information
    test_cases = [
        {
            "message": "John Anderson submitted a health insurance claim for hospitalization on October 15, 2024. Claim amount is $15,750.00 and has been approved.",
            "description": "Health insurance claim - Approved"
        },
        {
            "message": "Sarah Williams filed an auto insurance claim for vehicle accident on November 1, 2024. Damage cost is $8,500.00 and is pending review.",
            "description": "Auto insurance claim - Pending"
        },
        {
            "message": "Michael Brown's life insurance claim for $50,000.00 submitted on October 30, 2024 has been denied due to policy lapse.",
            "description": "Life insurance claim - Denied"
        }
    ]
    
    print(f"🎯 Using Model: azure_ai/genailab-maas-DeepSeek-V3-0324")
    print(f"🔗 Testing Endpoint: {url}")
    print("\n" + "-" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['description']}")
        print(f"Input: {test_case['message']}")
        
        try:
            # Send request to DeepSeek endpoint
            response = requests.post(
                url,
                json={
                    "message": test_case["message"],
                    "temperature": 0.1  # Low temperature for consistent structured output
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ SUCCESS!")
                print(f"Model Used: {result.get('model', 'Unknown')}")
                print(f"Status: {result.get('status', 'Unknown')}")
                
                # Display the generated JSON
                generated_json = result.get('generated_json', '')
                print(f"\n📊 Generated JSON:")
                print("-" * 40)
                print(generated_json)
                print("-" * 40)
                
                # Try to parse as JSON to validate structure
                try:
                    parsed_json = json.loads(generated_json)
                    print("✅ Valid JSON structure")
                    
                    # Check for required fields
                    required_fields = [
                        "Claim Number", "Status", "Policy Number", "Policy Type",
                        "Claimant Name", "Claim Date", "Incident Type", "Claim Amount"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in parsed_json]
                    if not missing_fields:
                        print("✅ All required fields present")
                    else:
                        print(f"⚠️ Missing fields: {missing_fields}")
                    
                    # Save result
                    filename = f"deepseek_result_case_{i}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(parsed_json, f, indent=2, ensure_ascii=False)
                    print(f"💾 Result saved to: {filename}")
                    
                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON format: {e}")
                    print("Raw response saved for debugging")
                    
            else:
                print(f"❌ FAILED: {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
        
        print("-" * 60)
    
    print("\n🎯 FOCUSED TEST COMPLETED")
    print("📝 Testing only the DeepSeek model endpoint for structured JSON output")

def test_model_connection():
    """Quick test of model connectivity"""
    print("\n🔍 Testing Model Connection...")
    
    try:
        response = requests.get("http://localhost:8000/api/v1/test-llm", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Model Connection Working")
            print(f"Model: {result.get('model', 'Unknown')}")
            print(f"Status: {result.get('status', 'Unknown')}")
            print(f"Response: {result.get('response', 'No response')[:100]}...")
            return True
        else:
            print(f"❌ Connection Failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Exception: {e}")
        return False

def main():
    """Run focused DeepSeek test"""
    print("🎯 DEEPSEEK MODEL FOCUSED TEST")
    print("Testing azure_ai/genailab-maas-DeepSeek-V3-0324 for structured JSON output")
    print("=" * 80)
    
    # Test basic connectivity first
    if test_model_connection():
        print("\n✅ Proceeding with DeepSeek JSON generation test...")
        test_deepseek_claim_json()
    else:
        print("\n❌ Skipping JSON test due to connectivity issues")
    
    print("\n" + "=" * 80)
    print("🎯 FOCUSED TEST SUMMARY")
    print("Objective: Test DeepSeek model for structured claim JSON generation")
    print("Expected: JSON with Claim Number, Status, Policy details, etc.")

if __name__ == "__main__":
    main()
