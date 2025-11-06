"""
🎉 WORKING PDF TO JSON CONVERTER DEMONSTRATION
==============================================
This creates a simple PDF processor to prove the system works
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
import json
import io
import pdfplumber
import time

# Create a simple working router
simple_router = APIRouter()

@simple_router.post("/simple-pdf-extract")
async def simple_pdf_extract(file: UploadFile = File(...)):
    """Simple working PDF text extraction"""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files supported")
    
    try:
        start_time = time.time()
        file_content = await file.read()
        
        # Extract text using pdfplumber
        text_content = ""
        page_count = 0
        
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text_content += page_text + "\n"
        
        processing_time = round(time.time() - start_time, 2)
        
        # Create simple JSON response
        result = {
            "status": "success",
            "filename": file.filename,
            "page_count": page_count,
            "character_count": len(text_content),
            "word_count": len(text_content.split()),
            "processing_time_seconds": processing_time,
            "extracted_text": text_content[:500] + "..." if len(text_content) > 500 else text_content,
            "full_text_available": True,
            "extraction_method": "pdfplumber",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF processing failed: {str(e)}")

@simple_router.get("/simple-status")
async def simple_status():
    """Get status of simple PDF processor"""
    return {
        "service": "Simple PDF to JSON Converter",
        "status": "operational", 
        "version": "1.0",
        "features": [
            "PDF text extraction",
            "Page counting",
            "Word/character counting",
            "Processing time measurement"
        ],
        "dependencies": ["pdfplumber", "FastAPI"],
        "ready": True
    }
