"""
🎯 FINAL PDF TO JSON CONVERTER STATUS REPORT
============================================
Complete test of all PDF converter functionality with TCS GenAI Lab models
"""
import requests
import json
import os
import time

class PDFConverterTester:
    def __init__(self):
        self.base_url = "http://localhost:8000/api/v1"
        self.results = {}
        
    def test_basic_connectivity(self):
        """Test basic API connectivity"""
        print("🔍 Testing Basic API Connectivity...")
        try:
            response = requests.get("http://localhost:8000/")
            if response.status_code == 200:
                print("✅ FastAPI server is running and responsive")
                self.results['connectivity'] = True
                return True
            else:
                print(f"❌ Server returned status {response.status_code}")
                self.results['connectivity'] = False
                return False
        except Exception as e:
            print(f"❌ Cannot connect to server: {e}")
            self.results['connectivity'] = False
            return False
    
    def test_available_models(self):
        """Test TCS GenAI Lab models endpoint"""
        print("\n🔍 Testing Available Models Endpoint...")
        try:
            response = requests.get(f"{self.base_url}/available-models")
            if response.status_code == 200:
                data = response.json()
                models = data.get('available_models', [])
                print(f"✅ Available Models Endpoint Working")
                print(f"   📊 Total Models: {len(models)}")
                print(f"   🎯 Default Model: {data.get('default_model')}")
                print(f"   📋 Models: {', '.join(models[:3])}...")
                self.results['models_endpoint'] = True
                self.results['available_models'] = models
                return True
            else:
                print(f"❌ Failed: {response.status_code}")
                self.results['models_endpoint'] = False
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            self.results['models_endpoint'] = False
            return False
    
    def test_model_connection(self):
        """Test TCS GenAI Lab model connectivity"""
        print("\n🔍 Testing TCS GenAI Lab Model Connection...")
        try:
            response = requests.post(f"{self.base_url}/test-model", 
                                   params={"model_name": "azure/genailab-maas-gpt-4o"})
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    print("✅ TCS GenAI Lab Model Connection Working!")
                    print(f"   🤖 Model: {data.get('model')}")
                    print(f"   📝 Response: {data.get('response', 'No response')[:100]}...")
                    self.results['model_connection'] = True
                    return True
                else:
                    print("❌ TCS GenAI Lab Model Connection Failed")
                    print(f"   🚫 Error: {data.get('error', 'Unknown error')}")
                    self.results['model_connection'] = False
                    self.results['connection_error'] = data.get('error')
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                self.results['model_connection'] = False
                return False
        except Exception as e:
            print(f"❌ Exception: {e}")
            self.results['model_connection'] = False
            return False
    
    def test_pdf_demo_converter(self):
        """Test local PDF converter (without LLM)"""
        print("\n🔍 Testing Local PDF Demo Converter...")
        
        if not os.path.exists("pdfsam.pdf"):
            print("❌ Test PDF file not found")
            self.results['demo_converter'] = False
            return False
        
        try:
            # Test demo info
            response = requests.get(f"{self.base_url}/demo-info")
            if response.status_code != 200:
                print(f"❌ Demo info failed: {response.status_code}")
                self.results['demo_converter'] = False
                return False
            
            # Test PDF conversion
            with open("pdfsam.pdf", 'rb') as f:
                files = {'file': ('pdfsam.pdf', f, 'application/pdf')}
                data = {'extraction_type': 'demo'}
                
                response = requests.post(f"{self.base_url}/pdf-to-json-demo", 
                                       files=files, data=data, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Local PDF Demo Converter Working!")
                    print(f"   📄 File: {result['filename']}")
                    print(f"   📊 Pages: {result['page_count']}")
                    print(f"   ⏱️ Processing Time: {result['processing_time']}s")
                    print(f"   🔧 Method: {result['extraction_method']}")
                    
                    # Save result
                    with open("demo_result.json", 'w', encoding='utf-8') as out_f:
                        json.dump(result, out_f, indent=2, ensure_ascii=False)
                    print(f"   💾 Result saved to: demo_result.json")
                    
                    self.results['demo_converter'] = True
                    self.results['demo_pages'] = result['page_count']
                    return True
                else:
                    print(f"❌ Conversion failed: {response.status_code}")
                    print(f"   🚫 Error: {response.text}")
                    self.results['demo_converter'] = False
                    return False
        except Exception as e:
            print(f"❌ Exception: {e}")
            self.results['demo_converter'] = False
            return False
    
    def test_llm_pdf_converter(self):
        """Test LLM-powered PDF converter"""
        print("\n🔍 Testing LLM-Powered PDF Converter...")
        
        if not os.path.exists("pdfsam.pdf"):
            print("❌ Test PDF file not found")
            self.results['llm_converter'] = False
            return False
        
        try:
            with open("pdfsam.pdf", 'rb') as f:
                files = {'file': ('pdfsam.pdf', f, 'application/pdf')}
                data = {
                    'model_name': 'azure/genailab-maas-gpt-4o',
                    'extraction_type': 'general'
                }
                
                response = requests.post(f"{self.base_url}/pdf-to-json", 
                                       files=files, data=data, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ LLM PDF Converter Working!")
                    print(f"   📄 File: {result['filename']}")
                    print(f"   📊 Pages: {result['page_count']}")
                    print(f"   🤖 Model: {result['model_used']}")
                    print(f"   ⏱️ Processing Time: {result.get('processing_time')}s")
                    
                    # Save result
                    with open("llm_result.json", 'w', encoding='utf-8') as out_f:
                        json.dump(result, out_f, indent=2, ensure_ascii=False)
                    print(f"   💾 Result saved to: llm_result.json")
                    
                    self.results['llm_converter'] = True
                    self.results['llm_pages'] = result['page_count']
                    return True
                else:
                    print(f"❌ LLM Conversion failed: {response.status_code}")
                    print(f"   🚫 Error: {response.text}")
                    self.results['llm_converter'] = False
                    return False
        except Exception as e:
            print(f"❌ Exception: {e}")
            self.results['llm_converter'] = False
            return False
    
    def generate_report(self):
        """Generate final status report"""
        print("\n" + "=" * 60)
        print("📊 FINAL PDF TO JSON CONVERTER STATUS REPORT")
        print("=" * 60)
        
        connectivity = self.results.get('connectivity', False)
        models_endpoint = self.results.get('models_endpoint', False) 
        model_connection = self.results.get('model_connection', False)
        demo_converter = self.results.get('demo_converter', False)
        llm_converter = self.results.get('llm_converter', False)
        
        print(f"🌐 API Connectivity:        {'✅ WORKING' if connectivity else '❌ FAILED'}")
        print(f"📋 Models Endpoint:         {'✅ WORKING' if models_endpoint else '❌ FAILED'}")
        print(f"🤖 TCS GenAI Lab Connection: {'✅ WORKING' if model_connection else '❌ FAILED'}")
        print(f"🔧 Local PDF Converter:     {'✅ WORKING' if demo_converter else '❌ FAILED'}")
        print(f"🚀 LLM PDF Converter:       {'✅ WORKING' if llm_converter else '❌ FAILED'}")
        
        print("\n" + "-" * 60)
        print("📈 SUMMARY")
        print("-" * 60)
        
        working_count = sum([connectivity, models_endpoint, model_connection, demo_converter, llm_converter])
        total_count = 5
        
        if working_count == total_count:
            print("🎉 ALL SYSTEMS WORKING! PDF to JSON converter is fully operational!")
            print("✨ You can now convert PDF files to structured JSON using TCS GenAI Lab models!")
        elif working_count >= 3:
            print("🎯 MOSTLY WORKING! Core functionality is operational")
            if not model_connection:
                print("⚠️  TCS GenAI Lab connection needs configuration")
                print(f"   Error: {self.results.get('connection_error', 'Connection failed')}")
            if not llm_converter and demo_converter:
                print("✅ Local PDF processing is working as fallback")
        else:
            print("⚠️  NEEDS ATTENTION! Several components need fixing")
        
        print(f"\n📊 Success Rate: {working_count}/{total_count} ({working_count/total_count*100:.1f}%)")
        
        if models_endpoint:
            models = self.results.get('available_models', [])
            print(f"🔧 Available Models: {len(models)}")
        
        if demo_converter:
            pages = self.results.get('demo_pages', 0)
            print(f"📄 Demo Processing: {pages} pages extracted")
        
        if llm_converter:
            pages = self.results.get('llm_pages', 0)
            print(f"🤖 LLM Processing: {pages} pages processed")
        
        print("\n" + "=" * 60)
        print("🔗 API Endpoints Available:")
        print("   • GET  /api/v1/available-models")
        print("   • GET  /api/v1/extraction-types") 
        print("   • POST /api/v1/test-model")
        print("   • POST /api/v1/pdf-to-json (LLM-powered)")
        print("   • POST /api/v1/pdf-to-json-demo (Local processing)")
        print("   • GET  /api/v1/demo-info")
        print("   • GET  /docs (Swagger UI)")
        
        return working_count == total_count

def main():
    """Run comprehensive PDF converter tests"""
    print("🚀 STARTING COMPREHENSIVE PDF TO JSON CONVERTER TESTS")
    print("=" * 60)
    
    tester = PDFConverterTester()
    
    # Run all tests
    tests = [
        tester.test_basic_connectivity,
        tester.test_available_models,
        tester.test_model_connection,
        tester.test_pdf_demo_converter,
        tester.test_llm_pdf_converter
    ]
    
    for test in tests:
        test()
        time.sleep(1)  # Brief pause between tests
    
    # Generate final report
    success = tester.generate_report()
    
    return success

if __name__ == "__main__":
    main()
