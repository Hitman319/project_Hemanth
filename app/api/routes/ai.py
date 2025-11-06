"""
AI-powered API Routes using LangChain and TCS GenAI Lab
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.core.config import settings

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    temperature: float = 0.7

class ChatResponse(BaseModel):
    response: str
    model: str

def get_llm_client():
    """Create and return configured LLM client"""
    # Create HTTP client with SSL verification disabled
    http_client = httpx.Client(verify=False)
    
    # Initialize ChatOpenAI with custom configuration
    llm = ChatOpenAI(
        base_url=settings.genai_base_url,
        model=settings.genai_model,
        api_key=settings.genai_api_key,
        http_client=http_client
    )
    return llm

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest) -> ChatResponse:
    """
    Chat with TCS GenAI Lab using LangChain
    """
    try:
        # Check if API key is available
        if not settings.genai_api_key:
            raise HTTPException(
                status_code=500, 
                detail="GenAI Lab API key not configured"
            )
        
        # Get LLM client
        llm = get_llm_client()
        
        # Create message and get response
        message = HumanMessage(content=request.message)
        response = await llm.ainvoke([message])
        
        return ChatResponse(
            response=response.content,
            model=settings.genai_model
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with GenAI Lab: {str(e)}"
        )

@router.get("/ai-hello/{name}", response_model=dict[str, str])
async def ai_powered_hello(name: str) -> dict[str, str]:
    """
    Generate a creative hello message using TCS GenAI Lab
    """
    try:
        if not settings.genai_api_key:
            raise HTTPException(
                status_code=500,
                detail="GenAI Lab API key not configured"
            )
        
        # Get LLM client
        llm = get_llm_client()
        
        prompt = f"Create a creative and friendly hello message for someone named {name}. Make it warm and personalized but keep it short (1-2 sentences)."
        message = HumanMessage(content=prompt)
        response = await llm.ainvoke([message])
        
        return {"message": response.content}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating AI response: {str(e)}"
        )

@router.get("/test-llm")
async def test_llm_connection():
    """
    Test the LLM connection - equivalent to your standalone script
    """
    try:
        if not settings.genai_api_key:
            raise HTTPException(
                status_code=500,
                detail="GenAI Lab API key not configured"
            )
        
        # Get LLM client
        llm = get_llm_client()
        
        # Test with "Hi" message like your example
        response = await llm.ainvoke("Hi")
        
        return {
            "status": "success",
            "message": "LLM connection successful",
            "response": response.content,
            "model": settings.genai_model,
            "base_url": settings.genai_base_url
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM connection failed: {str(e)}"
        )

@router.post("/generate-claim-json")
async def generate_claim_json(request: ChatRequest):
    """
    Generate structured claim JSON using DeepSeek model
    """
    try:
        if not settings.genai_api_key:
            raise HTTPException(
                status_code=500,
                detail="GenAI Lab API key not configured"
            )
        
        # Get LLM client with DeepSeek model
        llm = get_llm_client()
        
        # Create a prompt for structured claim data
        prompt = f"""
        Based on this input: "{request.message}"
        
        Generate a structured JSON response for insurance claim data with these exact fields:
        - Claim Number (format: #CLM-YYYY-XXX)
        - Status (APPROVED/PENDING/DENIED)
        - Policy Number (format: POL-XX-XXXXXX)
        - Policy Type (Health/Auto/Life etc.)
        - Claimant Name
        - Claim Date
        - Incident Type
        - Claim Amount (format: $X,XXX.XX)
        
        Return only valid JSON without any explanation or markdown formatting.
        """
        
        message = HumanMessage(content=prompt)
        response = await llm.ainvoke([message])
        
        return {
            "status": "success",
            "model": "azure_ai/genailab-maas-DeepSeek-V3-0324",
            "generated_json": response.content,
            "raw_response": response.content
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating claim JSON: {str(e)}"
        )

@router.post("/generate-claim-json-demo")
async def generate_claim_json_demo(request: ChatRequest):
    """
    Demo endpoint that generates the exact JSON format you specified
    (Works without external LLM connection for demonstration)
    """
    try:
        # Parse the input message to extract relevant information
        message = request.message.lower()
        
        # Demo logic to create structured JSON based on input
        # This demonstrates the exact format you want
        demo_claims = [
            {
                "Claim Number": "#CLM-2024-001",
                "Status": "APPROVED",
                "Policy Number": "POL-HD-789456",
                "Policy Type": "Health",
                "Claimant Name": "John Anderson",
                "Claim Date": "October 15, 2024", 
                "Incident Type": "Hospitalization",
                "Claim Amount": "$15,750.00"
            },
            {
                "Claim Number": "#CLM-2024-002", 
                "Status": "PENDING",
                "Policy Number": "POL-AU-567890",
                "Policy Type": "Auto",
                "Claimant Name": "Sarah Williams",
                "Claim Date": "November 1, 2024",
                "Incident Type": "Vehicle Accident", 
                "Claim Amount": "$8,500.00"
            },
            {
                "Claim Number": "#CLM-2024-003",
                "Status": "DENIED", 
                "Policy Number": "POL-LF-123456",
                "Policy Type": "Life",
                "Claimant Name": "Michael Brown",
                "Claim Date": "October 30, 2024",
                "Incident Type": "Policy Claim",
                "Claim Amount": "$50,000.00"
            }
        ]
        
        # Select appropriate demo claim based on input
        if "john" in message or "anderson" in message:
            selected_claim = demo_claims[0]
        elif "sarah" in message or "williams" in message or "auto" in message:
            selected_claim = demo_claims[1] 
        elif "michael" in message or "brown" in message or "life" in message:
            selected_claim = demo_claims[2]
        else:
            # Default to first claim
            selected_claim = demo_claims[0]
        
        return {
            "status": "success", 
            "model": "azure_ai/genailab-maas-DeepSeek-V3-0324 (Demo Mode)",
            "generated_json": selected_claim,
            "note": "This is a demo showing the exact JSON format. In production, this would be generated by the DeepSeek model.",
            "input_processed": request.message
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in demo endpoint: {str(e)}"
        )
