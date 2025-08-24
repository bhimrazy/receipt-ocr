import pytest
from unittest.mock import patch
import numpy as np
from src.tesseract_ocr.utils import perform_ocr


# Mocking cv2 and pytesseract
@patch("src.tesseract_ocr.utils.cv2")
@patch("src.tesseract_ocr.utils.pytesseract")
@patch("src.tesseract_ocr.utils.imutils")
def test_perform_ocr_success(mock_imutils, mock_pytesseract, mock_cv2):
    # Setup mocks
    mock_cv2.imdecode.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    mock_imutils.resize.return_value = np.zeros((50, 50, 3), dtype=np.uint8)
    mock_cv2.cvtColor.return_value = np.zeros((50, 50), dtype=np.uint8)
    mock_cv2.GaussianBlur.return_value = np.zeros((50, 50), dtype=np.uint8)
    mock_cv2.Canny.return_value = np.zeros((50, 50), dtype=np.uint8)

    # Mock contours to simulate a found receipt
    mock_contour = np.array(
        [[[0, 0]], [[0, 49]], [[49, 49]], [[49, 0]]], dtype=np.int32
    )
    mock_imutils.grab_contours.return_value = [mock_contour]
    mock_cv2.contourArea.return_value = 1000
    mock_cv2.arcLength.return_value = 200
    mock_cv2.approxPolyDP.return_value = mock_contour

    mock_pytesseract.image_to_string.return_value = "Extracted Text"

    # Call the function
    dummy_img_array = np.zeros(10, dtype=np.uint8)
    result = perform_ocr(dummy_img_array)

    # Assertions
    assert result == "Extracted Text"
    mock_cv2.imdecode.assert_called_once_with(dummy_img_array, mock_cv2.IMREAD_COLOR)
    mock_pytesseract.image_to_string.assert_called_once()


@patch("src.tesseract_ocr.utils.cv2")
@patch("src.tesseract_ocr.utils.pytesseract")
@patch("src.tesseract_ocr.utils.imutils")
def test_perform_ocr_no_receipt_outline(mock_imutils, mock_pytesseract, mock_cv2):
    # Setup mocks to simulate no receipt outline found
    mock_cv2.imdecode.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    mock_imutils.resize.return_value = np.zeros((50, 50, 3), dtype=np.uint8)
    mock_cv2.cvtColor.return_value = np.zeros((50, 50), dtype=np.uint8)
    mock_cv2.GaussianBlur.return_value = np.zeros((50, 50), dtype=np.uint8)
    mock_cv2.Canny.return_value = np.zeros((50, 50), dtype=np.uint8)

    # No contours found that approximate to 4 points
    mock_imutils.grab_contours.return_value = [
        np.array([[[0, 0], [1, 1], [2, 2]]], dtype=np.int32)
    ]  # A contour not of 4 points
    mock_cv2.contourArea.return_value = 1000
    mock_cv2.arcLength.return_value = 200
    mock_cv2.approxPolyDP.return_value = np.array(
        [[[0, 0], [1, 1], [2, 2]]], dtype=np.int32
    )  # Not 4 points

    dummy_img_array = np.zeros(10, dtype=np.uint8)
    with pytest.raises(Exception, match="Could not find receipt outline."):
        perform_ocr(dummy_img_array)
