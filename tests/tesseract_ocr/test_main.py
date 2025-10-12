import pytest
from unittest.mock import patch, MagicMock
import numpy as np


# Patch the main function to avoid argparse.parse_args() being called directly
@patch("src.tesseract_ocr.main.process_receipt_image")
@patch("src.tesseract_ocr.main.pytesseract")
@patch("src.tesseract_ocr.main.argparse.ArgumentParser")
@patch("src.tesseract_ocr.main.os.path.exists")
@patch("src.tesseract_ocr.main.cv2")
def test_main_success(
    mock_cv2,
    mock_os_path_exists,
    mock_argparse_parser,
    mock_pytesseract,
    mock_process,
    capsys,
):
    # Setup mocks
    mock_os_path_exists.return_value = True

    # Mock argparse to return a dummy image path
    mock_args = MagicMock()
    mock_args.image = "dummy_image.jpg"
    mock_argparse_parser.return_value.parse_args.return_value = mock_args

    # Mock cv2 for imread
    mock_cv2.imread.return_value = np.zeros((100, 100, 3), dtype=np.uint8)

    mock_process.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
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


@patch("src.tesseract_ocr.main.process_receipt_image")
@patch("src.tesseract_ocr.main.argparse.ArgumentParser")
@patch("src.tesseract_ocr.main.os.path.exists")
@patch("src.tesseract_ocr.main.cv2")
def test_main_no_receipt_outline(
    mock_cv2,
    mock_os_path_exists,
    mock_argparse_parser,
    mock_process,
):
    mock_os_path_exists.return_value = True

    mock_args = MagicMock()
    mock_args.image = "dummy_image.jpg"
    mock_argparse_parser.return_value.parse_args.return_value = mock_args

    mock_cv2.imread.return_value = np.zeros((100, 100, 3), dtype=np.uint8)

    mock_process.side_effect = Exception("Could not find suitable receipt outline. Try debugging your edge detection and contour steps.")

    from src.tesseract_ocr.main import main

    with pytest.raises(Exception, match="Could not find suitable receipt outline."):
        main()
