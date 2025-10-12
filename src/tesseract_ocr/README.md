# Tesseract OCR Engine

This folder hosts a script and a Docker-compose setup for performing Optical Character Recognition (OCR) on receipt images.

![image](https://github.com/bhimrazy/receipt-ocr/assets/46085301/305df68d-50d8-41d4-81d0-9324966fb6c9)

## Prerequisites

- Python 3.x
- Docker
- Docker-compose

## Installation

### Install uv

- [uv documentation](https://docs.astral.sh/uv/getting-started/installation/)
  `uv` is a fast Python package installer and resolver, written in Rust.

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or, via `pip`:

```bash
pip install uv
```

### Clone the repository

```bash
git clone https://github.com/bhimrazy/receipt-ocr.git
cd receipt-ocr
```

### Set up Python environment (if not using Docker)

- Install [tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)

```bash
# Create and activate a virtual environment
uv venv --python=3.12
source .venv/bin/activate  # For Windows, use .venv\Scripts\activate

# Install dependencies
uv pip install -r src/tesseract_ocr/requirements.txt
```

## Usage

### Running the script locally

#### `main.py`

The `main.py` script performs OCR on an input image of a receipt.

```bash
python src/tesseract_ocr/main.py -i images/receipt.jpg
```

Replace `images/receipt.jpg` with the path to your receipt image.

> Please ensure that the image is well-lit and that the edges of the receipt are clearly visible and detectable within the image.
> <img src="https://github.com/bhimrazy/receipt-ocr/assets/46085301/2ea009f0-9e15-42b2-9f15-063a8ec169f1" alt="Receipt Image" width="300" height="400">

### Using API via Docker-compose

The repository includes a Docker-compose setup for running the OCR engine as a service.

```bash
docker-compose -f src/tesseract_ocr/docker-compose.yml up
```

Once the service is up and running, you can perform OCR on receipt images by sending a POST request to `http://localhost:8000/ocr/` with the image file.

## API Endpoint

The OCR functionality can be accessed via a FastAPI endpoint:

- **POST** `/ocr/`: Upload a receipt image file to perform OCR. The response will contain the extracted text from the receipt.

Example usage with cURL:

```bash
curl -X 'POST' \
  'http://localhost:8000/ocr/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@images/paper-cash-sell-receipt-vector-23876532.jpg;type=image/jpeg'
```

## License

This project is licensed under the terms of the MIT license.

## References

- [Automatically OCR’ing Receipts and Scans](https://pyimagesearch.com/2021/10/27/automatically-ocring-receipts-and-scans/)
