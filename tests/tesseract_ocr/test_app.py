import os
from fastapi.testclient import TestClient
from src.tesseract_ocr.app import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the OCR API"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ocr_receipt_valid_image():
    # Path to a dummy image for testing
    image_path = "images/receipt.jpg"
    if not os.path.exists(image_path):
        # Fallback if the specific image is not found, though it should exist in the project
        image_path = "images/main-street-restaurant-receipt.jpeg"

    with open(image_path, "rb") as image_file:
        response = client.post(
            "/ocr/", files={"file": ("receipt.jpg", image_file, "image/jpeg")}
        )
    assert response.status_code == 200
    assert "result" in response.json()
    assert len(response.json()["result"]) > 0  # Expect some text to be extracted


def test_ocr_receipt_invalid_file_type():
    response = client.post(
        "/ocr/", files={"file": ("test.txt", b"this is not an image", "text/plain")}
    )
    assert (
        response.status_code == 200
    )  # The app returns 200 with an error message for invalid file type
    assert response.json() == {"error": "Uploaded file is not an image"}
