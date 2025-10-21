# Receipt OCR Engine

[![Build Status](https://github.com/bhimrazy/receipt-ocr/actions/workflows/receipt-ocr.yml/badge.svg)](https://github.com/bhimrazy/receipt-ocr/actions/workflows/receipt-ocr.yml)
[![Code Coverage](https://codecov.io/gh/bhimrazy/receipt-ocr/branch/main/graph/badge.svg)](https://codecov.io/gh/bhimrazy/receipt-ocr)
[![License](https://img.shields.io/github/license/bhimrazy/receipt-ocr)](https://github.com/bhimrazy/receipt-ocr/blob/main/LICENSE)

An efficient **OCR** engine for receipt image processing.

This repository provides a comprehensive solution for **Optical Character Recognition (OCR)** on receipt images, featuring both a dedicated Tesseract OCR module and a general receipt processing package using LLMs.

![image](https://github.com/bhimrazy/receipt-ocr/assets/46085301/305df68d-50d8-41d4-81d0-9324966fb6c9)

## Star History

<a href="https://star-history.com/#bhimrazy/receipt-ocr&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=bhimrazy/receipt-ocr&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=bhimrazy/receipt-ocr&type=Date&theme=dark" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=bhimrazy/receipt-ocr&type=Date" />
 </picture>
</a>

## Table of Contents

- [Receipt OCR Engine](#receipt-ocr-engine)
  - [Star History](#star-history)
  - [Table of Contents](#table-of-contents)
  - [Quick Start](#quick-start)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [How to Use Receipt OCR](#how-to-use-receipt-ocr)
    - [Receipt OCR Module (Structured Data Extraction)](#receipt-ocr-module-structured-data-extraction)
    - [Tesseract OCR Module (Raw Text Extraction)](#tesseract-ocr-module-raw-text-extraction)
  - [Troubleshooting](#troubleshooting)
  - [Contributing](#contributing)
  - [LinkedIn Post](#linkedin-post)
  - [License](#license)

## Quick Start

**Extract structured data from a receipt in 3 steps:**

1. **Install the package:**
   ```bash
   pip install receipt-ocr
   ```

2. **Set up your API key:**
   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   ```

3. **Process a receipt:**
   ```bash
   receipt-ocr images/receipt.jpg
   ```

For Docker or advanced usage, see [Usage Examples](#usage-examples) below.

## Project Structure

The project is organized into two main modules:

- **`src/receipt_ocr/`**: A new package for abstracting general receipt processing logic, including CLI, programmatic API, and a production [FastAPI web service](./app/) for LLM-powered structured data extraction from receipts.
- **`src/tesseract_ocr/`**: Contains the Tesseract OCR FastAPI application, CLI, utility functions, and Docker setup for performing raw OCR text extraction from images.

## Prerequisites

- Python 3.x
- Docker & Docker-compose(for running as a service)
- Tesseract OCR (for local Tesseract CLI usage) - [Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html)

## How to Use Receipt OCR

### Receipt OCR Module (Structured Data Extraction)

This module provides a higher-level abstraction for processing receipts, leveraging LLMs for parsing and extraction.

To use the `receipt-ocr` CLI, first install it:

```bash
pip install receipt-ocr
```

1.  **Configure Environment Variables:**
    Create a `.env` file in the project root or set environment variables directly. This module supports multiple LLM providers.

    **Supported Providers:**

    - **OpenAI:**
      > Get API key from: https://platform.openai.com/api-keys
      ```
      OPENAI_API_KEY="your_openai_api_key_here"
      OPENAI_MODEL="gpt-4o"
      ```

    - **Gemini (Google):**
      > Get API key from: https://aistudio.google.com/app/apikey
      ```
      OPENAI_API_KEY="your_gemini_api_key_here"
      OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
      OPENAI_MODEL="gemini-2.5-pro"
      ```

    - **Groq:**
      > Get API key from: https://console.groq.com/keys
      ```
      OPENAI_API_KEY="your_groq_api_key_here"
      OPENAI_BASE_URL="https://api.groq.com/openai/v1"
      OPENAI_MODEL="llama3-8b-8192"
      ```

2.  **Process a receipt using the `receipt-ocr` CLI:**

    ```bash
    receipt-ocr images/receipt.jpg
    ```

    This command will use the configured LLM provider to extract structured data from the receipt image.

    > sample output

    ```json
    {
      "merchant_name": "Saathimart.com",
      "merchant_address": "Narephat, Kathmandu",
      "transaction_date": "2024-05-07",
      "transaction_time": "09:09:00",
      "total_amount": 185.0,
      "line_items": [
        {
          "item_name": "COLGATE DENTAL",
          "item_quantity": 1,
          "item_price": 95.0,
          "item_total": 95.0
        },
        {
          "item_name": "PATANJALI ANTI",
          "item_quantity": 1,
          "item_price": 70.0,
          "item_total": 70.0
        },
        {
          "item_name": "GODREJ NO 1 SOAP",
          "item_quantity": 1,
          "item_price": 20.0,
          "item_total": 20.0
        }
      ]
    }
    ```

3.  **Using Receipt OCR Programmatically in Python:**

    You can also use the `receipt-ocr` library directly in your Python code:

    ```python
    from receipt_ocr.processors import ReceiptProcessor
    from receipt_ocr.providers import OpenAIProvider

    # Initialize the provider
    provider = OpenAIProvider(api_key="your_api_key", base_url="your_base_url")

    # Initialize the processor
    processor = ReceiptProcessor(provider)

    # Define the JSON schema for extraction
    json_schema = {
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

    # Process the receipt
    result = processor.process_receipt("path/to/receipt.jpg", json_schema, "gpt-4.1")

    print(result)
    ```

    **Advanced Usage with Response Format Types:**

    For compatibility with different LLM providers, you can specify the response format type:

    ```python
    result = processor.process_receipt(
        "path/to/receipt.jpg", 
        json_schema, 
        "gpt-4.1", 
        response_format_type="json_object"  # or "json_schema", "text"
    )
    ```

    Supported `response_format_type` values:
    - `"json_object"` (default) - Standard JSON object format
    - `"json_schema"` - Structured JSON schema format (for newer OpenAI APIs)
    - `"text"` - Plain text responses

    <details>
    <summary>Using <code>json_schema</code> format</summary>

    When using `response_format_type="json_schema"`, you must provide a proper JSON Schema object (not the simple dictionary format). The library handles the OpenAI API boilerplate, so you just need to pass the schema definition.

    Example proper JSON Schema:

    ```python
    json_schema = {
      "type": "object",
      "properties": {
        "merchant_name": {"type": "string"},
        "merchant_address": {"type": "string"},
        "transaction_date": {"type": "string"},
        "transaction_time": {"type": "string"},
        "total_amount": {"type": "number"},
        "line_items": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "item_name": {"type": "string"},
              "item_quantity": {"type": "number"},
              "item_price": {"type": "number"}
            },
            "required": ["item_name", "item_quantity", "item_price"],
            "additionalProperties": false
          }
        }
      },
      "required": [
        "merchant_name",
        "merchant_address",
        "transaction_date",
        "transaction_time",
        "total_amount",
        "line_items"
      ],
      "additionalProperties": false
    }
    ```

    See the [OpenAI structured outputs documentation](https://platform.openai.com/docs/guides/structured-outputs) for more information.

    </details>

4.  **Run Receipt OCR as a Docker web service:**

    For a production-ready REST API, use the FastAPI web service:

    ```bash
    docker compose -f app/docker-compose.yml up
    ```

    The service provides REST endpoints for receipt processing:

    - `GET /health` - Health check
    - `POST /ocr/` - Process receipt images with optional custom JSON schemas

    **Example API usage:**

    ```bash
    # Health check
    curl http://localhost:8000/health

    # Process receipt with default schema
    curl -X POST "http://localhost:8000/ocr/" \
      -F "file=@images/receipt.jpg"

    # Process with custom schema
    curl -X POST "http://localhost:8000/ocr/" \
      -F "file=@images/receipt.jpg" \
      -F 'json_schema={"merchant": "string", "total": "number"}'
    ```

    For detailed API documentation, visit `http://localhost:8000/docs` when the service is running.

### Tesseract OCR Module (Raw Text Extraction)

This module provides direct OCR capabilities using Tesseract. For more detailed local setup and usage, refer to [`src/tesseract_ocr/README.md`](src/tesseract_ocr/README.md).

1.  **Run Tesseract OCR locally via CLI:**

    ```bash
    python src/tesseract_ocr/main.py -i images/receipt.jpg
    ```

    Replace `images/receipt.jpg` with the path to your receipt image.

    > Please ensure that the image is well-lit and that the edges of the receipt are clearly visible and detectable within the image.
    > <img src="https://github.com/bhimrazy/receipt-ocr/assets/46085301/2ea009f0-9e15-42b2-9f15-063a8ec169f1" alt="Receipt Image" width="300" height="400">

2.  **Run Tesseract OCR as a Docker service:**

    ```bash
    docker compose -f src/tesseract_ocr/docker-compose.yml up
    ```

    Once the service is up and running, you can perform OCR on receipt images by sending a POST request to `http://localhost:8000/ocr/` with the image file.

    **API Endpoint:**

    - **POST** `/ocr/`: Upload a receipt image file to perform OCR. The response will contain the extracted text from the receipt.

    > **Note:** The Tesseract OCR API returns raw extracted text from the receipt image. For structured JSON output with parsed fields such as merchant name, line items, and totals, use the `receipt-ocr` instead.

    **Example usage with cURL:**

    ```bash
    curl -X 'POST' \
      'http://localhost:8000/ocr/' \
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'file=@images/paper-cash-sell-receipt-vector-23876532.jpg;type=image/jpeg'
    ```

## Troubleshooting

**Common Issues and Solutions:**

- **API Key Errors:** Ensure your `OPENAI_API_KEY` is set correctly and has sufficient credits. Check the provider's dashboard for key status.

- **Model Not Found:** Verify the `OPENAI_MODEL` matches available models for your provider. For OpenAI, check https://platform.openai.com/docs/models.

- **Poor OCR Results:** Use high-quality, well-lit images. Ensure receipt text is clear and not skewed.

- **Installation Issues:** If `pip install receipt-ocr` fails, try `pip install --upgrade pip` first.

- **Docker Issues:** Ensure Docker is running and ports 8000 are available.

For more help, check the [GitHub Issues](https://github.com/bhimrazy/receipt-ocr/issues) or create a new issue.

## Contributing

We welcome contributions to the Receipt OCR Engine! To contribute, please follow these steps:

1.  **Fork the repository** and clone it to your local machine.
2.  **Create a new branch** for your feature or bug fix.
3.  **Set up your development environment**:

    ```bash
    # Navigate to the project root
    cd receipt-ocr

    # Install uv
    curl -LsSf https://astral.sh/uv/install.sh | sh # OR pip install uv

    # Create and activate a virtual environment
    uv venv --python=3.12
    source .venv/bin/activate  # For Windows, use .venv\Scripts\activate

    # Install development and test dependencies
    uv sync --all-extras --dev
    uv pip install -e.
    
    # Optional: Install requirements for the tesseract_ocr module
    uv pip install -r src/tesseract_ocr/requirements.txt
    ```

4.  **Make your changes** and ensure they adhere to the project's coding style.
5.  **Run tests** to ensure your changes haven't introduced any regressions:
    ```bash
    # Run tests for the receipt_ocr module
    uv run pytest tests/receipt_ocr
    
    # Run tests for the tesseract_ocr module  
    uv run pytest tests/tesseract_ocr
    ```
6.  **Run linting and formatting checks**:
    ```bash
    uvx ruff check .
    uvx ruff format .
    ```
7.  **Commit your changes** with a clear and concise commit message.
8.  **Push your branch** to your forked repository.
9.  **Open a Pull Request** to the `main` branch of the upstream repository, describing your changes in detail.

## LinkedIn Post

- Gemini Docs: https://ai.google.dev/tutorials/python_quickstart
- LinkedIn Post: https://www.linkedin.com/feed/update/urn:li:activity:7145860319150505984/

![image](https://github.com/bhimrazy/receipt-ocr/assets/46085301/ee4a0c82-f134-4a19-a275-93a59c7503b8)

## License

This project is licensed under the terms of the MIT license.
