"""
Live Test for PDF to JSON Converter with TCS GenAI Lab
"""
import requests
import json
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
PDF_FILE = "pdfsam.pdf"  # Sample PDF file in the project

def test_available_models():
    """Test getting available models"""
    print("🔍 Testing available models...")
    response = requests.get(f"{BASE_URL}/available-models")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Available models: {len(data['available_models'])}")
        print(f"✅ Default model: {data['default_model']}")
        for model in data['available_models']:
            print(f"   - {model}")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_extraction_types():
    """Test getting extraction types"""
    print("\n🔍 Testing extraction types...")
    response = requests.get(f"{BASE_URL}/extraction-types")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Extraction types: {len(data['extraction_types'])}")
        for ext_type, description in data['extraction_types'].items():
            print(f"   - {ext_type}: {description}")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_model_connection(model="azure/genailab-maas-gpt-4o"):
    """Test model connection"""
    print(f"\n🔍 Testing model connection: {model}...")
    response = requests.post(f"{BASE_URL}/test-model", params={"model_name": model})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Connection status: {data['status']}")
        print(f"✅ Model response: {data.get('response', 'No response')}")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_pdf_conversion():
    """Test PDF to JSON conversion"""
    print(f"\n🔍 Testing PDF conversion with {PDF_FILE}...")
    
    if not os.path.exists(PDF_FILE):
        print(f"❌ PDF file {PDF_FILE} not found")
        return False
    
    # Test with different extraction types
    extraction_types = ["general", "structured", "tables", "forms"]
    
    for extraction_type in extraction_types:
        print(f"\n   Testing extraction type: {extraction_type}")
        
        with open(PDF_FILE, 'rb') as f:
            files = {'file': (PDF_FILE, f, 'application/pdf')}
            data = {
                'model_name': 'azure/genailab-maas-gpt-4o',
                'extraction_type': extraction_type
            }
            
            response = requests.post(f"{BASE_URL}/pdf-to-json", files=files, data=data)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success! Pages processed: {result['page_count']}")
                print(f"   ✅ Model used: {result['model_used']}")
                print(f"   ✅ Processing time: {result.get('processing_time', 'N/A')}s")
                
                # Save result to file for inspection
                output_file = f"pdf_result_{extraction_type}.json"
                with open(output_file, 'w', encoding='utf-8') as out_f:
                    json.dump(result, out_f, indent=2, ensure_ascii=False)
                print(f"   ✅ Result saved to: {output_file}")
                
            else:
                print(f"   ❌ Error: {response.text}")
                return False
    
    return True

def test_custom_prompt():
    """Test PDF conversion with custom prompt"""
    print(f"\n🔍 Testing PDF conversion with custom prompt...")
    
    if not os.path.exists(PDF_FILE):
        print(f"❌ PDF file {PDF_FILE} not found")
        return False
    
    custom_prompt = "Extract only key headings and any numerical data. Format as a simple summary."
    
    with open(PDF_FILE, 'rb') as f:
        files = {'file': (PDF_FILE, f, 'application/pdf')}
        data = {
            'model_name': 'azure/genailab-maas-gpt-4o',
            'extraction_type': 'general',
            'custom_prompt': custom_prompt
        }
        
        response = requests.post(f"{BASE_URL}/pdf-to-json", files=files, data=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Custom extraction completed")
            print(f"✅ Model used: {result['model_used']}")
            
            # Save result to file for inspection
            output_file = "pdf_result_custom.json"
            with open(output_file, 'w', encoding='utf-8') as out_f:
                json.dump(result, out_f, indent=2, ensure_ascii=False)
            print(f"✅ Result saved to: {output_file}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False

def main():
    """Run all tests"""
    print("🚀 Starting PDF to JSON Converter Live Tests")
    print("=" * 50)
    
    tests = [
        ("Available Models", test_available_models),
        ("Extraction Types", test_extraction_types),
        ("Model Connection", test_model_connection),
        ("PDF Conversion", test_pdf_conversion),
        ("Custom Prompt", test_custom_prompt)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! PDF to JSON converter is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()
