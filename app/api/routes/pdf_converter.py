"""
PDF to JSON Converter using TCS GenAI Lab LLM Models
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import httpx
import json
import io
import pdfplumber
import PyPDF2
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.core.config import settings

router = APIRouter()

class PDFProcessRequest(BaseModel):
    model_name: Optional[str] = "azure/genailab-maas-gpt-4o"
    extraction_type: Optional[str] = "general"  # general, structured, tables, forms
    custom_prompt: Optional[str] = None
    
class PDFProcessResponse(BaseModel):
    status: str
    filename: str
    model_used: str
    extracted_data: Dict[Any, Any]
    page_count: int
    processing_time: Optional[float]

def get_llm_client(model_name: str = None):
    """Create and return configured LLM client with specified model"""
    if not model_name:
        model_name = settings.genai_model
        
    # Validate model availability
    if model_name not in settings.available_models:
        raise HTTPException(
            status_code=400, 
            detail=f"Model '{model_name}' not available. Choose from: {settings.available_models}"
        )
    
    # Create HTTP client with SSL verification disabled
    http_client = httpx.Client(verify=False)
    
    # Initialize ChatOpenAI with custom configuration
    llm = ChatOpenAI(
        base_url=settings.genai_base_url,
        model=model_name,
        api_key=settings.genai_api_key,
        http_client=http_client,
        temperature=0.1  # Lower temperature for more consistent extraction
    )
    return llm

def extract_text_from_pdf(file_content: bytes) -> Dict[str, Any]:
    """Extract text from PDF using multiple methods"""
    extracted_data = {
        "pages": [],
        "total_pages": 0,
        "full_text": "",
        "metadata": {}
    }
    
    try:
        # Method 1: Using pdfplumber (better for complex layouts)
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            extracted_data["total_pages"] = len(pdf.pages)
            
            for i, page in enumerate(pdf.pages):
                page_data = {
                    "page_number": i + 1,
                    "text": page.extract_text() or "",
                    "tables": [],
                    "images_count": len(page.images) if hasattr(page, 'images') else 0
                }
                
                # Extract tables if any
                tables = page.extract_tables()
                if tables:
                    for j, table in enumerate(tables):
                        page_data["tables"].append({
                            "table_id": j + 1,
                            "data": table
                        })
                
                extracted_data["pages"].append(page_data)
                extracted_data["full_text"] += page_data["text"] + "\n"
                
    except Exception as e:
        # Fallback to PyPDF2
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            extracted_data["total_pages"] = len(pdf_reader.pages)
            
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                page_data = {
                    "page_number": i + 1,
                    "text": page_text,
                    "tables": [],
                    "images_count": 0
                }
                extracted_data["pages"].append(page_data)
                extracted_data["full_text"] += page_text + "\n"
                
        except Exception as e2:
            raise HTTPException(status_code=400, detail=f"Failed to extract PDF content: {str(e2)}")
    
    return extracted_data

def get_extraction_prompt(extraction_type: str, custom_prompt: str = None) -> str:
    """Get appropriate prompt based on extraction type"""
    
    if custom_prompt:
        return custom_prompt
    
    prompts = {
        "general": """
        Extract and structure the content from this PDF text into a well-organized JSON format. 
        Include the following structure:
        {
            "document_type": "type of document",
            "title": "document title",
            "summary": "brief summary",
            "main_content": {
                "sections": [
                    {
                        "section_title": "title",
                        "content": "content text",
                        "subsections": []
                    }
                ]
            },
            "key_information": {
                "dates": [],
                "names": [],
                "numbers": [],
                "locations": []
            },
            "metadata": {
                "language": "detected language",
                "estimated_reading_time": "time in minutes"
            }
        }
        """,
        
        "structured": """
        Extract structured data from this document and organize it into a hierarchical JSON format.
        Focus on identifying:
        - Headers and subheaders
        - Lists and bullet points
        - Key-value pairs
        - Tables and structured data
        - Contact information
        - Dates and numbers
        
        Return a clean, well-structured JSON that preserves the document's organization.
        """,
        
        "tables": """
        Focus on extracting tabular data from this document. Structure the response as:
        {
            "tables": [
                {
                    "table_id": 1,
                    "title": "table title if available",
                    "headers": ["column1", "column2", ...],
                    "rows": [
                        ["value1", "value2", ...],
                        ["value1", "value2", ...]
                    ]
                }
            ],
            "non_tabular_content": "other important content"
        }
        """,
        
        "forms": """
        Extract form data and fields from this document. Structure as:
        {
            "form_type": "type of form",
            "fields": [
                {
                    "field_name": "name",
                    "field_type": "text/number/date/checkbox",
                    "value": "extracted value",
                    "required": true/false
                }
            ],
            "sections": [
                {
                    "section_name": "section",
                    "fields": []
                }
            ]
        }
        """
    }
    
    return prompts.get(extraction_type, prompts["general"])

@router.post("/pdf-to-json", response_model=PDFProcessResponse)
async def convert_pdf_to_json(
    file: UploadFile = File(...),
    model_name: Optional[str] = Form("azure/genailab-maas-gpt-4o"),
    extraction_type: Optional[str] = Form("general"),
    custom_prompt: Optional[str] = Form(None)
):
    """
    Convert PDF file to structured JSON using TCS GenAI Lab LLM models
    
    - **file**: PDF file to process
    - **model_name**: LLM model to use for extraction
    - **extraction_type**: Type of extraction (general, structured, tables, forms)
    - **custom_prompt**: Custom extraction prompt (optional)
    """
    import time
    start_time = time.time()
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Check API key
    if not settings.genai_api_key:
        raise HTTPException(status_code=500, detail="GenAI Lab API key not configured")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Extract text from PDF
        pdf_data = extract_text_from_pdf(file_content)
        
        if not pdf_data["full_text"].strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
        
        # Get LLM client
        llm = get_llm_client(model_name)
        
        # Prepare extraction prompt
        extraction_prompt = get_extraction_prompt(extraction_type, custom_prompt)
        
        # Create the full prompt
        full_prompt = f"""
        {extraction_prompt}
        
        PDF Content to process:
        {pdf_data["full_text"][:8000]}  # Limit to first 8000 chars to avoid token limits
        
        Please return only valid JSON format without any additional text or markdown formatting.
        """
        
        # Process with LLM
        message = HumanMessage(content=full_prompt)
        response = await llm.ainvoke([message])
        
        # Parse LLM response as JSON
        try:
            extracted_json = json.loads(response.content.strip())
        except json.JSONDecodeError:
            # If direct JSON parsing fails, try to extract JSON from response
            content = response.content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            try:
                extracted_json = json.loads(content.strip())
            except json.JSONDecodeError:
                # If still fails, wrap the response
                extracted_json = {
                    "raw_response": response.content,
                    "parsing_error": "Could not parse as JSON",
                    "pdf_metadata": {
                        "pages": pdf_data["total_pages"],
                        "has_tables": any(page.get("tables") for page in pdf_data["pages"])
                    }
                }
        
        # Add metadata to the response
        extracted_json["pdf_metadata"] = {
            "total_pages": pdf_data["total_pages"],
            "extraction_method": extraction_type,
            "model_used": model_name,
            "processing_time_seconds": round(time.time() - start_time, 2)
        }
        
        return PDFProcessResponse(
            status="success",
            filename=file.filename,
            model_used=model_name,
            extracted_data=extracted_json,
            page_count=pdf_data["total_pages"],
            processing_time=round(time.time() - start_time, 2)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )

@router.get("/available-models")
async def get_available_models():
    """Get list of available LLM models for PDF processing"""
    return {
        "available_models": settings.available_models,
        "default_model": settings.genai_model,
        "model_info": {
            "azure/genailab-maas-gpt-35-turbo": "Fast, cost-effective for simple extractions",
            "azure/genailab-maas-gpt-4o": "High-quality, recommended for complex documents", 
            "azure/genailab-maas-gpt-4o-mini": "Balanced performance and speed",
            "azure_ai/genailab-maas-DeepSeek-R1": "Advanced reasoning capabilities",
            "azure_ai/genailab-maas-Llama-3.3-70B-Instruct": "Large context, good for long documents",
            "gemini-2.5-pro": "Google's advanced model with multimodal capabilities"
        }
    }

@router.get("/extraction-types")
async def get_extraction_types():
    """Get available extraction types and their descriptions"""
    return {
        "extraction_types": {
            "general": "General document extraction with sections, key info, and metadata",
            "structured": "Focus on hierarchical structure, headers, lists, and organization", 
            "tables": "Specialized table extraction and tabular data processing",
            "forms": "Form field extraction and form data processing"
        },
        "custom_prompt_supported": True,
        "example_custom_prompt": "Extract only the financial data and convert currencies to USD format"
    }

@router.post("/test-model")
async def test_model_connection(model_name: str = "azure/genailab-maas-gpt-4o"):
    """Test connection to a specific model"""
    try:
        if not settings.genai_api_key:
            raise HTTPException(status_code=500, detail="GenAI Lab API key not configured")
        
        llm = get_llm_client(model_name)
        
        test_message = HumanMessage(content="Respond with a simple JSON: {'status': 'working', 'model': 'model_name'}")
        response = await llm.ainvoke([test_message])
        
        return {
            "status": "success",
            "model": model_name,
            "response": response.content,
            "connection": "working"
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "model": model_name,
            "error": str(e),
            "connection": "failed"
        }
