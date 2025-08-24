# Receipt OCR Engine

[![Build Status](https://github.com/bhimrazy/receipt-ocr/actions/workflows/receipt-ocr.yml/badge.svg)](https://github.com/bhimrazy/receipt-ocr/actions/workflows/receipt-ocr.yml)
[![Code Coverage](https://codecov.io/gh/bhimrazy/receipt-ocr/branch/main/graph/badge.svg)](https://codecov.io/gh/bhimrazy/receipt-ocr)
[![License](https://img.shields.io/github/license/bhimrazy/receipt-ocr)](https://github.com/bhimrazy/receipt-ocr/blob/main/LICENSE)

An efficient OCR engine for receipt image processing.

This repository provides a comprehensive solution for Optical Character Recognition (OCR) on receipt images, featuring both a dedicated Tesseract OCR module and a general receipt processing package using LLMs.

![image](https://github.com/bhimrazy/receipt-ocr/assets/46085301/305df68d-50d8-41d4-81d0-9324966fb6c9)

## Star History

<a href="https://star-history.com/#bhimrazy/receipt-ocr&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=bhimrazy/receipt-ocr&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=bhimrazy/receipt-ocr&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=bhimrazy/receipt-ocr&type=Date" />
 </picture>
</a>

## Project Structure

The project is organized into two main modules:

- **`src/receipt_ocr/`**: A new package for abstracting general receipt processing logic, including CLI, parsers, prompts, and providers for various LLM services.
- **`src/tesseract_ocr/`**: Contains the Tesseract OCR FastAPI application, CLI, utility functions, and Docker setup for performing OCR.

## Prerequisites

- Python 3.x
- Docker (for running Tesseract OCR as a service)
- Docker-compose (for running Tesseract OCR as a service)
- Tesseract OCR (for local Tesseract CLI usage) - [Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html)

## Usage Examples

### Receipt OCR Module

This module provides a higher-level abstraction for processing receipts, leveraging LLMs for parsing and extraction.

To use the `receipt-ocr` CLI, first install it:

```bash
pip install receipt-ocr
```

1.  **Configure Environment Variables:**
    Create a `.env` file in the project root or set environment variables directly. This module supports multiple LLM providers.

    Example `.env` for OpenAI:

    > Get it from here: http://platform.openai.com/api-keys

    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    OPENAI_MODEL="gpt-4.1"
    ```

    Example `.env` for Gemini:

    > Get it from here: https://aistudio.google.com/app/apikey

    ```
    OPENAI_API_KEY="your_gemini_api_key_here"
    OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
    OPENAI_MODEL="gemini-2.5-pro"
    ```

    Example `.env` for Groq:

    > Get it from here: https://console.groq.com/keys

    ```
    OPENAI_API_KEY="your_groq_api_key_here"
    OPENAI_BASE_URL="https://api.groq.com/openai/v1/models"
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

### Tesseract OCR Module

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
    docker-compose -f src/tesseract_ocr/docker-compose.yml up
    ```

    Once the service is up and running, you can perform OCR on receipt images by sending a POST request to `http://localhost:8000/ocr/` with the image file.

    **API Endpoint:**

    - **POST** `/ocr/`: Upload a receipt image file to perform OCR. The response will contain the extracted text from the receipt.

    **Example usage with cURL:**

    ```bash
    curl -X 'POST' \
      'http://localhost:8000/ocr/' \
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'file=@images/paper-cash-sell-receipt-vector-23876532.jpg;type=image/jpeg'
    ```

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
    uv pip install -r src/tesseract_ocr/requirements.txt
    uv pip install -e.
    ```

4.  **Make your changes** and ensure they adhere to the project's coding style.
5.  **Run tests** to ensure your changes haven't introduced any regressions:
    ```bash
    uv run pytest
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

## References

- [Automatically OCR’ing Receipts and Scans](https://pyimagesearch.com/2021/10/27/automatically-ocring-receipts-and-scans/)
