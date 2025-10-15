from unittest.mock import MagicMock, patch

import pytest

from receipt_ocr import OpenAIProvider


@patch("receipt_ocr.providers.OpenAI")
def test_get_response(mock_openai_client_class, dummy_image_path, mock_chat_completion):
    # Configure the mock OpenAI client that will be used by OpenAIProvider
    mock_openai_instance = MagicMock()
    mock_openai_client_class.return_value = mock_openai_instance

    provider = OpenAIProvider(api_key="test_api_key", base_url="http://test.com")

    mock_chat_completion.choices[
        0
    ].message.content = '{"merchant_name": "Test Merchant"}'
    mock_openai_instance.chat.completions.create.return_value = mock_chat_completion

    dummy_json_schema = {
        "type": "object",
        "properties": {"merchant_name": {"type": "string"}},
    }
    response = provider.get_response(
        dummy_image_path, json_schema=dummy_json_schema, model="gpt-4o"
    )

    assert response.choices[0].message.content == '{"merchant_name": "Test Merchant"}'


@patch("receipt_ocr.providers.OpenAI")
def test_get_response_api_error(mock_openai_client_class, dummy_image_path):
    mock_openai_instance = MagicMock()
    mock_openai_client_class.return_value = mock_openai_instance
    mock_openai_instance.chat.completions.create.side_effect = Exception("API Error")

    provider = OpenAIProvider(api_key="test_api_key")

    dummy_json_schema = {"type": "object"}

    with pytest.raises(Exception, match="API Error"):
        provider.get_response(
            dummy_image_path, json_schema=dummy_json_schema, model="gpt-4o"
        )
