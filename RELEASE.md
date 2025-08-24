# Release v0.2.0

## Overview

This release introduces a significant refactoring of the project structure, separating Tesseract OCR functionalities into a dedicated module and establishing a new `receipt_ocr` package for LLM-powered receipt processing. It also includes various enhancements to documentation, environment configuration, and CI/CD workflows.

## Key Changes

### ✨ Features

*   **Modular Project Structure:** Introduced `src/tesseract_ocr/` for Tesseract-specific components and `src/receipt_ocr/` for general receipt processing with LLMs.
*   **LLM-Powered Receipt Parsing:** Enhanced receipt parsing capabilities by integrating Large Language Models for structured data extraction.
*   **Line Item Totals:** Added `item_total` field to line items in the receipt extraction prompt for more detailed output.

### 🚀 Enhancements

*   **Improved Environment Configuration:** Updated `.env.example` with clearer variable names for Gemini and Groq LLM providers.
*   **Comprehensive README:** Reworked the main `README.md` to include a detailed project overview, installation instructions, usage examples for both modules, and a new contributing guide.
*   **Tesseract Module Documentation:** Added a link to `src/tesseract_ocr/README.md` for detailed local setup and usage of the Tesseract OCR module.

### ⚙️ Refactoring

*   **Codebase Reorganization:** Moved Tesseract OCR FastAPI application, CLI, utilities, and Docker setup into `src/tesseract_ocr/`.
*   **New Receipt OCR Package:** Created `src/receipt_ocr/` with `cli.py`, `parsers.py`, `prompts.py`, and `providers.py`.

### 🧪 Tests & CI/CD

*   **Expanded Test Coverage:** Added unit tests for `src/tesseract_ocr/main.py` and `src/tesseract_ocr/utils.py`.
*   **Robust Temporary File Handling:** Improved existing tests for `src/receipt_ocr/providers.py` using `pytest`'s `tmp_path` fixture.
*   **CI Workflow Updates:** Adjusted GitHub Actions workflows (`tesseract-ocr.yml`, `receipt-ocr.yml`) for correct Tesseract installation and `PYTHONPATH` settings.

### 📚 Documentation

*   **Contributing Guide:** Added a new section in `README.md` detailing how to contribute to the project.
*   **Updated Project Metadata:** Refreshed `LICENSE` copyright year and added GitHub issue/PR templates.

## Installation & Upgrade

To install or upgrade to this version, follow the instructions in the main [`README.md`](README.md) file.

## What's Next

We are continuously working on improving the OCR accuracy, expanding LLM integration options, and enhancing the overall user experience. Stay tuned for more updates!
