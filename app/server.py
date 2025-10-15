import os
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from receipt_ocr.processors import ReceiptProcessor

# Initialize processor once (not on each request)
processor = ReceiptProcessor()

app = FastAPI(
    title="Receipt OCR API",
    description="Extract structured data from receipt images using LLM",
    version="1.0.0",
)

# Default JSON schema (same as CLI)
DEFAULT_SCHEMA = {
    "merchant_name": "string",
    "merchant_address": "string",
    "transaction_date": "string",
    "transaction_time": "string",
    "total_amount": "number",
    "line_items": [
        {
            "item_name": "string",
            "item_quantity": "number",
            "item_price": "number",
        }
    ],
}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


class OCRRequest(BaseModel):
    """Request model for OCR processing."""
    schema: Optional[Dict] = None


@app.get("/")
async def root():
    return {
        "message": "Receipt OCR API - Extract structured data from receipts",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "POST /ocr/": "Extract structured data from receipt image",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "receipt-ocr-api"}


@app.post("/ocr/")
async def ocr_receipt(
    file: UploadFile,
    schema: Optional[Dict] = None,
):
    """
    Extract structured data from a receipt image using LLM processing.

    - **file**: Receipt image file (JPEG, PNG, etc., max 5MB)
    - **schema**: Optional custom JSON schema as dict
    """
    try:
        # Validation: Check content type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Validation: Check file size (5MB limit)
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Seek back to beginning

        if file_size > MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=413, detail="Image too large. Max 5 MB allowed."
            )

        image_bytes = file.file.read()

        # Use provided schema or default
        json_schema = schema if schema is not None else DEFAULT_SCHEMA

        # Use model from environment
        llm_model = os.getenv("OPENAI_MODEL", "gpt-4o")

        # Process the receipt using the processor
        result = processor.process_receipt_bytes(image_bytes, json_schema, llm_model)

        # Add metadata
        result["_metadata"] = {
            "model_used": llm_model,
            "custom_schema": schema is not None,
            "processing_time": "N/A",  # Could add timing later
        }

        return JSONResponse(content=result, status_code=200)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
