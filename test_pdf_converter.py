"""
Test script for PDF to JSON converter
"""
import asyncio
import httpx
from app.core.config import settings
from app.api.routes.pdf_converter import get_llm_client

async def test_pdf_converter_setup():
    """Test the PDF converter setup and model connections"""
    
    print("🔧 Testing PDF to JSON Converter Setup...")
    print(f"Base URL: {settings.genai_base_url}")
    print(f"Default Model: {settings.genai_model}")
    print(f"API Key configured: {'Yes' if settings.genai_api_key else 'No'}")
    print(f"Available models: {len(settings.available_models)}")
    
    # Test model connection
    try:
        print("\n🤖 Testing model connection...")
        llm = get_llm_client("azure/genailab-maas-gpt-4o")
        
        from langchain_core.messages import HumanMessage
        test_message = HumanMessage(content="Respond with: {'status': 'working', 'test': 'success'}")
        response = await llm.ainvoke([test_message])
        
        print(f"✅ Model response: {response.content}")
        print("✅ PDF converter is ready!")
        
        return True
        
    except Exception as e:
        print(f"❌ Model connection failed: {str(e)}")
        return False

async def test_sample_text_extraction():
    """Test text extraction and JSON conversion with sample text"""
    
    print("\n📄 Testing text to JSON conversion...")
    
    sample_text = """
    INVOICE
    Company: TCS Limited
    Date: 2024-01-15
    Invoice Number: INV-001
    
    Bill To:
    Customer Name: ABC Corp
    Address: 123 Business Street
    
    Items:
    1. Software Development - $5000
    2. Consulting Services - $3000
    3. Training - $2000
    
    Total: $10,000
    """
    
    try:
        llm = get_llm_client("azure/genailab-maas-gpt-4o")
        
        prompt = """
        Extract the following information from this invoice text and return as JSON:
        {
            "document_type": "invoice",
            "invoice_number": "number",
            "company": "company name",
            "customer": "customer name", 
            "date": "date",
            "items": [
                {"description": "item", "amount": "amount"}
            ],
            "total": "total amount"
        }
        
        Text to process:
        """ + sample_text
        
        from langchain_core.messages import HumanMessage
        message = HumanMessage(content=prompt)
        response = await llm.ainvoke([message])
        
        print("📋 Extracted JSON:")
        print(response.content)
        print("✅ Text extraction test successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Text extraction test failed: {str(e)}")
        return False

if __name__ == "__main__":
    async def main():
        print("🚀 PDF to JSON Converter Test Suite")
        print("=" * 50)
        
        # Test 1: Basic setup
        setup_ok = await test_pdf_converter_setup()
        
        if setup_ok:
            # Test 2: Sample text extraction
            await test_sample_text_extraction()
        else:
            print("⚠️ Setup test failed, skipping text extraction test")
        
        print("\n" + "=" * 50)
        print("🏁 Test suite completed!")
    
    asyncio.run(main())
