import json
from unittest.mock import patch, MagicMock
from receipt_ocr.cli import main


@patch("receipt_ocr.cli.ReceiptProcessor")
@patch("receipt_ocr.cli.OpenAIProvider")
@patch("builtins.open")
@patch("json.load")
def test_main_with_custom_schema(
    mock_json_load, mock_open, mock_provider_class, mock_processor_class, tmp_path
):
    # Mock the schema file
    mock_json_load.return_value = {
        "type": "object",
        "properties": {"test": {"type": "string"}},
    }

    # Mock the processor
    mock_processor_instance = MagicMock()
    mock_processor_instance.process_receipt.return_value = {"test": "value"}
    mock_processor_class.return_value = mock_processor_instance

    # Mock the provider
    mock_provider_instance = MagicMock()
    mock_provider_class.return_value = mock_provider_instance

    # Create a dummy image
    image_path = tmp_path / "test.png"
    image_path.write_bytes(b"dummy")

    schema_path = tmp_path / "schema.json"
    schema_path.write_text("{}")

    with patch(
        "sys.argv",
        [
            "cli.py",
            str(image_path),
            "--schema_path",
            str(schema_path),
            "--model",
            "gpt-4",
        ],
    ):
        with patch("builtins.print") as mock_print:
            main()

    mock_open.assert_called_once_with(str(schema_path), "r")
    mock_json_load.assert_called_once()
    mock_provider_class.assert_called_once_with(api_key=None, base_url=None)
    mock_processor_class.assert_called_once_with(mock_provider_instance)
    mock_processor_instance.process_receipt.assert_called_once_with(
        str(image_path),
        {"type": "object", "properties": {"test": {"type": "string"}}},
        "gpt-4",
    )
    mock_print.assert_called_once_with(json.dumps({"test": "value"}, indent=4))


@patch("receipt_ocr.cli.ReceiptProcessor")
@patch("receipt_ocr.cli.OpenAIProvider")
def test_main_with_default_schema(mock_provider_class, mock_processor_class, tmp_path):
    # Mock the processor
    mock_processor_instance = MagicMock()
    mock_processor_instance.process_receipt.return_value = {"merchant_name": "Test"}
    mock_processor_class.return_value = mock_processor_instance

    # Mock the provider
    mock_provider_instance = MagicMock()
    mock_provider_class.return_value = mock_provider_instance

    # Create a dummy image
    image_path = tmp_path / "test.png"
    image_path.write_bytes(b"dummy")

    with patch("sys.argv", ["cli.py", str(image_path)]):
        with patch("builtins.print") as mock_print:
            main()

    mock_provider_class.assert_called_once_with(api_key=None, base_url=None)
    mock_processor_class.assert_called_once_with(mock_provider_instance)
    # Check that default schema is used
    call_args = mock_processor_instance.process_receipt.call_args
    assert call_args[0][1]["merchant_name"] == "string"
    mock_print.assert_called_once_with(json.dumps({"merchant_name": "Test"}, indent=4))


@patch("receipt_ocr.cli.ReceiptProcessor")
@patch("receipt_ocr.cli.OpenAIProvider")
def test_main_with_api_key_and_base_url(
    mock_provider_class, mock_processor_class, tmp_path
):
    # Mock the processor
    mock_processor_instance = MagicMock()
    mock_processor_instance.process_receipt.return_value = {}
    mock_processor_class.return_value = mock_processor_instance

    # Mock the provider
    mock_provider_instance = MagicMock()
    mock_provider_class.return_value = mock_provider_instance

    # Create a dummy image
    image_path = tmp_path / "test.png"
    image_path.write_bytes(b"dummy")

    with patch(
        "sys.argv",
        [
            "cli.py",
            str(image_path),
            "--api_key",
            "test_key",
            "--base_url",
            "http://test.com",
        ],
    ):
        with patch("builtins.print"):
            main()

    mock_provider_class.assert_called_once_with(
        api_key="test_key", base_url="http://test.com"
    )
