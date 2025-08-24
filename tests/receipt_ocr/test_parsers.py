import pytest
from receipt_ocr import ReceiptParser


@pytest.fixture
def parser():
    return ReceiptParser()


def test_parse_valid_json_with_json_block(parser):
    response = """```json
{
    "merchant_name": "Test Merchant",
    "total_amount": 10.00
}
```"""
    parsed = parser.parse(response)
    assert parsed["merchant_name"] == "Test Merchant"
    assert parsed["total_amount"] == 10.00


def test_parse_valid_json_with_block(parser):
    response = """```
{
    "merchant_name": "Test Merchant",
    "total_amount": 10.00
}
```"""
    parsed = parser.parse(response)
    assert parsed["merchant_name"] == "Test Merchant"
    assert parsed["total_amount"] == 10.00


def test_parse_valid_json_string(parser):
    response = """{
    "merchant_name": "Test Merchant",
    "total_amount": 10.00
}"""
    parsed = parser.parse(response)
    assert parsed["merchant_name"] == "Test Merchant"
    assert parsed["total_amount"] == 10.00


def test_parse_invalid_json(parser):
    response = "not a valid json string"
    parsed = parser.parse(response)
    assert "error" in parsed
