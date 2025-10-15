# Receipt OCR API

A FastAPI service that extracts structured data from receipt images using Large Language Models (LLMs).

## Features

- **LLM-powered extraction**: Uses OpenAI-compatible APIs for accurate receipt parsing
- **Structured JSON output**: Returns merchant info, line items, totals, and dates
- **Custom schemas**: Support for custom JSON schemas
- **File validation**: Validates image files and sizes (max 5MB)
- **RESTful API**: Clean FastAPI endpoints with automatic documentation

## Quick Start

### 1. Install Dependencies

```bash
# Install uv (if not already installed)
pip install uv

# Install dependencies
uv sync
```

### 2. Set Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY="your_openai_api_key_here"
OPENAI_MODEL="gpt-4o"
OPENAI_BASE_URL="https://api.openai.com/v1"  # Optional
```

# Run the API

```bash
# Using uv run
uv run fastapi run server.py

# Or using Docker (from app directory)
cd app
docker compose up
```

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Process a receipt (default schema)
curl -X POST "http://localhost:8000/ocr/" \
  -F "file=@path/to/receipt.jpg"

# Process with custom schema
curl -X POST "http://localhost:8000/ocr/" \
  -F "file=@path/to/receipt.jpg" \
  -F 'json_schema={"merchant": "string", "total": "number"}'
```

## API Endpoints

### `GET /`
Returns API information and available endpoints.

### `GET /health`
Health check endpoint.

### `POST /ocr/`
Extract structured data from a receipt image.

**Parameters:**
- `file` (required): Receipt image file (JPEG, PNG, etc., max 5MB)
- `json_schema` (optional): Custom JSON schema as dictionary

**Response:**
```json
{
  "merchant_name": "Store Name",
  "merchant_address": "123 Main St",
  "transaction_date": "2024-01-01",
  "total_amount": 25.99,
  "line_items": [
    {
      "item_name": "Product Name",
      "item_quantity": 1,
      "item_price": 25.99
    }
  ]
}
```

## Configuration

The API uses the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: "gpt-4o")
- `OPENAI_BASE_URL`: Custom API base URL (optional)

## Development

### API Documentation

When running, visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

### Project Structure

```
app/
├── server.py          # FastAPI application
├── pyproject.toml     # Dependencies and build config
└── README.md         # This file
```

## License

MIT License
