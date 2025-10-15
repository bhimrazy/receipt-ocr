import json
from typing import Optional

from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.responses import JSONResponse

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
    json_schema: Optional[str] = Form(default=None),
):
    """Extract structured data from a receipt image using LLM processing.

    - **file**: Receipt image file (JPEG, PNG, etc., max 5MB)
    - **json_schema**: Optional custom JSON schema as string (will be parsed to dict)
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

        # Parse json_schema if provided
        schema_to_use = DEFAULT_SCHEMA
        if json_schema:
            try:
                schema_to_use = json.loads(json_schema)
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=400, detail="Invalid JSON schema format"
                )

        # Process the receipt using the processor
        result = processor.process_receipt(image_bytes, schema_to_use)
        return JSONResponse(content=result, status_code=200)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
