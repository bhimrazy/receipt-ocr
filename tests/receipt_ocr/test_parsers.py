import pytest
from receipt_ocr import ReceiptParser


@pytest.fixture
def parser():
    return ReceiptParser()


@pytest.mark.parametrize(
    "response",
    [
        """```json
{
    "merchant_name": "Test Merchant",
    "total_amount": 10.00
}
```""",
        """```
{
    "merchant_name": "Test Merchant",
    "total_amount": 10.00
}
```""",
        """{
    "merchant_name": "Test Merchant",
    "total_amount": 10.00
}""",
    ],
)
def test_parse_valid_json(parser, response):
    parsed = parser.parse(response)
    assert parsed["merchant_name"] == "Test Merchant"
    assert parsed["total_amount"] == 10.00


def test_parse_invalid_json(parser):
    response = "not a valid json string"
    parsed = parser.parse(response)
    assert "error" in parsed


def test_parse_empty_string(parser):
    response = ""
    parsed = parser.parse(response)
    assert "error" in parsed


def test_parse_malformed_code_block(parser):
    response = """```json
{
    "merchant_name": "Test Merchant",
    "total_amount": 10.00
"""
    parsed = parser.parse(response)
    assert "error" in parsed


def test_parse_partial_json(parser):
    response = """{
    "merchant_name": "Test Merchant"
"""
    parsed = parser.parse(response)
    assert "error" in parsed
