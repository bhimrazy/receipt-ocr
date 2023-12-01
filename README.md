# Receipt OCR Engine

This repository hosts a script and a Docker-compose setup for performing Optical Character Recognition (OCR) on receipt images.

## Prerequisites

- Python 3.x
- Docker
- Docker-compose

## Installation

### Clone the repository

```bash
git clone https://github.com/bhimrazy/receipt-ocr.git
cd receipt-ocr
```

### Set up Python environment (if not using Docker)
- Install tesseract

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # For Windows, use venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the script locally

#### `main.py`

The `main.py` script performs OCR on an input image of a receipt.

```bash
python main.py -i path/to/your/image.jpg
```

Replace `path/to/your/image.jpg` with the path to your receipt image.

### Using Docker-compose

The repository includes a Docker-compose setup for running the OCR engine as a service.

```bash
docker-compose up
```

Once the service is up and running, you can perform OCR on receipt images by sending a POST request to `http://localhost:8000/ocr/` with the image file.

## API Endpoint

The OCR functionality can be accessed via a FastAPI endpoint:

- **POST** `/ocr/`: Upload a receipt image file to perform OCR. The response will contain the extracted text from the receipt.

Example usage with cURL:

```bash
$curl -X 'POST' \
  'http://localhost:8000/ocr/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@images/paper-cash-sell-receipt-vector-23876532.jpg;type=image/jpeg'
```

## License

This project is licensed under the terms of the MIT license.

## References
- [Automatically OCR’ing Receipts and Scans](https://pyimagesearch.com/2021/10/27/automatically-ocring-receipts-and-scans/)


