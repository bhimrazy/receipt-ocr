import json

from receipt_ocr.prompts import SYSTEM_PROMPT, USER_PROMPT


def test_system_prompt_formatting():
    """Test that SYSTEM_PROMPT can be formatted with json_schema_content."""
    json_schema = {
        "type": "object",
        "properties": {
            "merchant_name": {"type": "string"},
            "total_amount": {"type": "number"},
        },
    }
    json_schema_str = json.dumps(json_schema, indent=2)

    # This should not raise an exception
    formatted_prompt = SYSTEM_PROMPT.format(json_schema_content=json_schema_str)

    assert "merchant_name" in formatted_prompt
    assert "total_amount" in formatted_prompt
    assert json_schema_str in formatted_prompt


def test_system_prompt_formatting_empty_schema():
    """Test SYSTEM_PROMPT formatting with minimal schema."""
    json_schema = {"type": "object"}
    import json

    json_schema_str = json.dumps(json_schema, indent=2)

    formatted_prompt = SYSTEM_PROMPT.format(json_schema_content=json_schema_str)

    assert json_schema_str in formatted_prompt


def test_user_prompt_is_string():
    """Test that USER_PROMPT is a non-empty string."""
    assert isinstance(USER_PROMPT, str)
    assert len(USER_PROMPT) > 0
