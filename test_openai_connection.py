"""
Simple test script to verify OpenAI API key works
"""
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.core.config import settings

async def test_openai_connection():
    """Test the OpenAI API connection"""
    try:
        print("🔑 Testing OpenAI API Key...")
        print(f"API Key starts with: {settings.openai_api_key[:10]}...")
        
        # Initialize ChatOpenAI
        llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-3.5-turbo",
            openai_api_key=settings.openai_api_key
        )
        
        # Test message
        message = HumanMessage(content="Say 'Hello from FastAPI!' in a creative way")
        print("📤 Sending test message to OpenAI...")
        
        response = await llm.ainvoke([message])
        print("📥 Response received!")
        print(f"🤖 AI Response: {response.content}")
        print("✅ OpenAI API connection successful!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Please check your API key and internet connection")

if __name__ == "__main__":
    asyncio.run(test_openai_connection())
