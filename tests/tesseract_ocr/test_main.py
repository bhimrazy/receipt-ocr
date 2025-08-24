import pytest
from unittest.mock import patch, MagicMock
import numpy as np


# Patch the main function to avoid argparse.parse_args() being called directly
@patch("src.tesseract_ocr.main.argparse.ArgumentParser")
@patch("src.tesseract_ocr.main.os.path.exists")
@patch("src.tesseract_ocr.main.cv2")
@patch("src.tesseract_ocr.main.imutils")
@patch("src.tesseract_ocr.main.pytesseract")
def test_main_success(
    mock_pytesseract,
    mock_imutils,
    mock_cv2,
    mock_os_path_exists,
    mock_argparse_parser,
    capsys,
):
    # Setup mocks
    mock_os_path_exists.return_value = True

    # Mock argparse to return a dummy image path
    mock_args = MagicMock()
    mock_args.image = "dummy_image.jpg"
    mock_argparse_parser.return_value.parse_args.return_value = mock_args

    # Mock cv2 and imutils for image processing
    mock_cv2.imread.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
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

    mock_pytesseract.image_to_string.return_value = "Extracted Text from Main"

    # Import and call main after patching
    from src.tesseract_ocr.main import main

    main()

    # Assertions
    mock_os_path_exists.assert_called_once_with("dummy_image.jpg")
    mock_cv2.imread.assert_called_once_with("dummy_image.jpg")
    mock_pytesseract.image_to_string.assert_called_once()

    # Capture stdout to check print statements
    captured = capsys.readouterr()
    assert "[INFO] raw output:" in captured.out
    assert "Extracted Text from Main" in captured.out


@patch("src.tesseract_ocr.main.argparse.ArgumentParser")
@patch("src.tesseract_ocr.main.os.path.exists")
def test_main_image_not_found(mock_os_path_exists, mock_argparse_parser):
    mock_os_path_exists.return_value = False

    mock_args = MagicMock()
    mock_args.image = "non_existent_image.jpg"
    mock_argparse_parser.return_value.parse_args.return_value = mock_args

    from src.tesseract_ocr.main import main

    with pytest.raises(Exception, match="The given image does not exist."):
        main()


@patch("src.tesseract_ocr.main.argparse.ArgumentParser")
@patch("src.tesseract_ocr.main.os.path.exists")
@patch("src.tesseract_ocr.main.cv2")
@patch("src.tesseract_ocr.main.imutils")
@patch("src.tesseract_ocr.main.pytesseract")
def test_main_no_receipt_outline(
    mock_pytesseract,
    mock_imutils,
    mock_cv2,
    mock_os_path_exists,
    mock_argparse_parser,
):
    mock_os_path_exists.return_value = True

    mock_args = MagicMock()
    mock_args.image = "dummy_image.jpg"
    mock_argparse_parser.return_value.parse_args.return_value = mock_args

    mock_cv2.imread.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    mock_imutils.resize.return_value = np.zeros((50, 50, 3), dtype=np.uint8)
    mock_cv2.cvtColor.return_value = np.zeros((50, 50), dtype=np.uint8)
    mock_cv2.GaussianBlur.return_value = np.zeros((50, 50), dtype=np.uint8)
    mock_cv2.Canny.return_value = np.zeros((50, 50), dtype=np.uint8)

    # No contours found that approximate to 4 points
    mock_imutils.grab_contours.return_value = [
        np.array([[[0, 0], [1, 1], [2, 2]]], dtype=np.int32)
    ]
    mock_cv2.contourArea.return_value = 1000
    mock_cv2.arcLength.return_value = 200
    mock_cv2.approxPolyDP.return_value = np.array(
        [[[0, 0], [1, 1], [2, 2]]], dtype=np.int32
    )

    from src.tesseract_ocr.main import main

    with pytest.raises(Exception, match="Could not find receipt outline."):
        main()
