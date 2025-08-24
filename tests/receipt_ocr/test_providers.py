from unittest.mock import patch, MagicMock
from receipt_ocr import OpenAIProvider


@patch("receipt_ocr.providers.OpenAI")
def test_get_response(mock_openai_client_class, tmp_path):
    # Configure the mock OpenAI client that will be used by OpenAIProvider
    mock_openai_instance = MagicMock()
    mock_openai_client_class.return_value = mock_openai_instance

    provider = OpenAIProvider(api_key="test_api_key", base_url="http://test.com")

    mock_choice = MagicMock()
    mock_choice.message.content = '{"merchant_name": "Test Merchant"}'
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_openai_instance.chat.completions.create.return_value = mock_response

    from PIL import Image

    # Create a dummy image file
    dummy_image = Image.new("RGB", (10, 10), color="red")
    image_path = tmp_path / "dummy_receipt.png"
    dummy_image.save(image_path)

    dummy_json_schema = {
        "type": "object",
        "properties": {"merchant_name": {"type": "string"}},
    }
    response = provider.get_response(
        str(image_path), json_schema=dummy_json_schema, model="gpt-4o"
    )

    assert response == '{"merchant_name": "Test Merchant"}'
