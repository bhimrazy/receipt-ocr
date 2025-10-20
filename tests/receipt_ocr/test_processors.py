import pytest
from unittest.mock import MagicMock
from receipt_ocr import ReceiptProcessor, OpenAIProvider, ReceiptParser


@pytest.fixture
def mock_provider():
    provider = MagicMock(spec=OpenAIProvider)
    return provider


@pytest.fixture
def mock_parser():
    parser = MagicMock(spec=ReceiptParser)
    return parser


@pytest.fixture
def processor(mock_provider, mock_parser):
    return ReceiptProcessor(provider=mock_provider, parser=mock_parser)


def test_process_receipt_success(
    processor, mock_provider, mock_parser, mock_chat_completion
):
    # Arrange
    mock_provider.get_response.return_value = mock_chat_completion
    mock_parser.parse.return_value = {"merchant_name": "Test Merchant", "total": 10.00}

    json_schema = {
        "type": "object",
        "properties": {
            "merchant_name": {"type": "string"},
            "total": {"type": "number"},
        },
    }

    # Act
    result = processor.process_receipt("dummy_path.png", json_schema, "gpt-4o")

    # Assert
    mock_provider.get_response.assert_called_once_with(
        "dummy_path.png", json_schema, "gpt-4o", None
    )
    mock_parser.parse.assert_called_once_with(
        '{"merchant_name": "Test Merchant", "total": 10.00}'
    )
    assert result == {"merchant_name": "Test Merchant", "total": 10.00}


def test_process_receipt_parser_error(
    processor, mock_provider, mock_parser, mock_chat_completion_error
):
    # Arrange
    mock_provider.get_response.return_value = mock_chat_completion_error
    mock_parser.parse.return_value = {"error": "Invalid JSON"}

    json_schema = {"type": "object"}

    # Act
    result = processor.process_receipt("dummy_path.png", json_schema, "gpt-4o")

    # Assert
    assert result == {"error": "Invalid JSON"}


def test_process_receipt_with_minimal_schema(
    processor, mock_provider, mock_parser, mock_chat_completion
):
    # Arrange
    mock_provider.get_response.return_value = mock_chat_completion
    mock_parser.parse.return_value = {"key": "value"}

    json_schema = {"type": "object", "properties": {"key": {"type": "string"}}}

    # Act
    result = processor.process_receipt("dummy_path.png", json_schema, "gpt-4o")

    # Assert
    assert result == {"key": "value"}
