"""
PDF Converter Demo - Local Processing Without LLM
This version extracts PDF content and shows structured JSON without requiring LLM connection
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import json
import io
import pdfplumber
import PyPDF2
import time

demo_router = APIRouter()

class PDFDemoResponse(BaseModel):
    status: str
    filename: str
    extraction_method: str
    extracted_data: Dict[Any, Any]
    page_count: int
    processing_time: float

def extract_pdf_content_demo(file_content: bytes) -> Dict[str, Any]:
    """Extract and structure PDF content without LLM processing"""
    extracted_data = {
        "document_summary": {
            "total_pages": 0,
            "total_characters": 0,
            "has_tables": False,
            "has_images": False
        },
        "pages": [],
        "full_text": "",
        "tables": [],
        "metadata": {}
    }
    
    try:
        # Method 1: Using pdfplumber (better for complex layouts)
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            extracted_data["document_summary"]["total_pages"] = len(pdf.pages)
            
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                page_data = {
                    "page_number": i + 1,
                    "text": page_text,
                    "character_count": len(page_text),
                    "tables": [],
                    "images_count": len(page.images) if hasattr(page, 'images') else 0
                }
                
                # Check for images
                if page_data["images_count"] > 0:
                    extracted_data["document_summary"]["has_images"] = True
                
                # Extract tables if any
                tables = page.extract_tables()
                if tables:
                    extracted_data["document_summary"]["has_tables"] = True
                    for j, table in enumerate(tables):
                        table_data = {
                            "table_id": f"page_{i+1}_table_{j+1}",
                            "page": i + 1,
                            "rows": len(table),
                            "columns": len(table[0]) if table else 0,
                            "data": table
                        }
                        page_data["tables"].append(table_data)
                        extracted_data["tables"].append(table_data)
                
                extracted_data["pages"].append(page_data)
                extracted_data["full_text"] += page_text + "\n\n"
                extracted_data["document_summary"]["total_characters"] += len(page_text)
                
        # Add some basic analysis
        text = extracted_data["full_text"]
        extracted_data["basic_analysis"] = {
            "word_count": len(text.split()),
            "line_count": len(text.split('\n')),
            "contains_email": "@" in text,
            "contains_phone": any(char.isdigit() for char in text) and ("phone" in text.lower() or "tel" in text.lower()),
            "contains_url": "http" in text.lower() or "www" in text.lower(),
            "language_hints": {
                "english_indicators": sum(1 for word in ["the", "and", "of", "to", "a"] if word in text.lower()),
                "numeric_content": sum(1 for char in text if char.isdigit()) / len(text) if text else 0
            }
        }
                
    except Exception as e:
        # Fallback to PyPDF2
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            extracted_data["document_summary"]["total_pages"] = len(pdf_reader.pages)
            extracted_data["extraction_method"] = "PyPDF2 (fallback)"
            
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                page_data = {
                    "page_number": i + 1,
                    "text": page_text,
                    "character_count": len(page_text),
                    "tables": [],
                    "images_count": 0,
                    "extraction_note": "Extracted using PyPDF2 fallback method"
                }
                
                extracted_data["pages"].append(page_data)
                extracted_data["full_text"] += page_text + "\n\n"
                extracted_data["document_summary"]["total_characters"] += len(page_text)
                
        except Exception as fallback_error:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to extract PDF content. Primary error: {str(e)}, Fallback error: {str(fallback_error)}"
            )
    
    return extracted_data

@demo_router.post("/pdf-to-json-demo", response_model=PDFDemoResponse)
async def convert_pdf_demo(
    file: UploadFile = File(...),
    extraction_type: str = "demo"
):
    """
    Demo PDF to JSON converter - Local processing without LLM
    Extracts text, tables, and metadata from PDF files
    """
    start_time = time.time()
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Extract content from PDF
        pdf_data = extract_pdf_content_demo(file_content)
        
        if not pdf_data["full_text"].strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
        
        # Create structured output
        structured_output = {
            "document_info": {
                "filename": file.filename,
                "pages": pdf_data["document_summary"]["total_pages"],
                "total_characters": pdf_data["document_summary"]["total_characters"],
                "word_count": pdf_data["basic_analysis"]["word_count"],
                "has_tables": pdf_data["document_summary"]["has_tables"],
                "has_images": pdf_data["document_summary"]["has_images"]
            },
            "extraction_summary": {
                "method": "Local extraction (pdfplumber + PyPDF2)",
                "extraction_type": extraction_type,
                "success": True,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "content": {
                "pages": pdf_data["pages"],
                "tables": pdf_data["tables"],
                "full_text": pdf_data["full_text"][:1000] + "..." if len(pdf_data["full_text"]) > 1000 else pdf_data["full_text"]
            },
            "analysis": pdf_data["basic_analysis"]
        }
        
        return PDFDemoResponse(
            status="success",
            filename=file.filename,
            extraction_method="Local PDF processing (demo mode)",
            extracted_data=structured_output,
            page_count=pdf_data["document_summary"]["total_pages"],
            processing_time=round(time.time() - start_time, 2)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)} - Type: {type(e).__name__}"
        )

@demo_router.get("/demo-info")
async def get_demo_info():
    """Get information about the demo PDF converter"""
    return {
        "name": "PDF to JSON Demo Converter",
        "description": "Local PDF processing without LLM dependency",
        "features": [
            "Text extraction from all pages",
            "Table detection and extraction", 
            "Basic document analysis",
            "Metadata extraction",
            "Fallback extraction methods"
        ],
        "supported_files": ["PDF"],
        "processing_method": "Local (pdfplumber + PyPDF2)",
        "llm_required": False,
        "demo_mode": True
    }
