"""
Test PDF Demo Converter - Working Version Without LLM
"""
import requests
import json
import os

def test_demo_pdf_converter():
    """Test the demo PDF converter that works without LLM"""
    print("🚀 Testing PDF Demo Converter (No LLM Required)")
    print("=" * 50)
    
    if not os.path.exists("pdfsam.pdf"):
        print("❌ PDF file pdfsam.pdf not found")
        return False
    
    # Test demo info endpoint
    print("🔍 Testing demo info endpoint...")
    response = requests.get("http://localhost:8000/api/v1/demo-info")
    if response.status_code == 200:
        info = response.json()
        print("✅ Demo info loaded")
        print(f"   Name: {info['name']}")
        print(f"   LLM Required: {info['llm_required']}")
        print(f"   Features: {len(info['features'])}")
    else:
        print(f"❌ Demo info failed: {response.status_code}")
        return False
    
    # Test PDF conversion
    print("\n🔍 Testing PDF conversion...")
    with open("pdfsam.pdf", 'rb') as f:
        files = {'file': ('pdfsam.pdf', f, 'application/pdf')}
        data = {'extraction_type': 'demo'}
        
        response = requests.post("http://localhost:8000/api/v1/pdf-to-json-demo", files=files, data=data)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ PDF Conversion Successful!")
            print(f"   📄 File: {result['filename']}")
            print(f"   📊 Pages: {result['page_count']}")
            print(f"   ⏱️ Processing Time: {result['processing_time']}s")
            print(f"   🔧 Method: {result['extraction_method']}")
            
            # Save result for inspection
            with open("pdf_demo_result.json", 'w', encoding='utf-8') as out_f:
                json.dump(result, out_f, indent=2, ensure_ascii=False)
            print(f"   💾 Result saved to: pdf_demo_result.json")
            
            # Show some extracted data
            extracted = result['extracted_data']
            doc_info = extracted['document_info']
            print(f"   📈 Analysis:")
            print(f"      - Total Characters: {doc_info['total_characters']}")
            print(f"      - Word Count: {doc_info['word_count']}")
            print(f"      - Has Tables: {doc_info['has_tables']}")
            print(f"      - Has Images: {doc_info['has_images']}")
            
            return True
        else:
            print(f"❌ Conversion failed: {response.text}")
            return False

if __name__ == "__main__":
    success = test_demo_pdf_converter()
    print("\n" + "=" * 50)
    if success:
        print("🎉 PDF Demo Converter is working perfectly!")
        print("📋 This demonstrates PDF to JSON conversion without LLM dependency")
        print("🔧 You can enhance this with TCS GenAI Lab integration later")
    else:
        print("❌ Demo test failed")
