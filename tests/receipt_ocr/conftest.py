from unittest.mock import MagicMock
import pytest
from PIL import Image


@pytest.fixture
def mock_chat_completion():
    """Reusable mock for OpenAI ChatCompletion response."""
    mock_choice = MagicMock()
    mock_choice.message.content = '{"merchant_name": "Test Merchant", "total": 10.00}'
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    return mock_response


@pytest.fixture
def mock_chat_completion_error():
    """Reusable mock for error response."""
    mock_choice = MagicMock()
    mock_choice.message.content = "invalid json"
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    return mock_response


@pytest.fixture
def dummy_image_path(tmp_path):
    """Create a dummy image file for testing."""
    dummy_image = Image.new("RGB", (10, 10), color="red")
    image_path = tmp_path / "dummy_receipt.png"
    dummy_image.save(image_path)
    return str(image_path)
