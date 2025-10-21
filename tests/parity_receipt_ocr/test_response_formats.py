#!/usr/bin/env python3
"""Integration test script for testing different response format types.

This script tests the receipt OCR processor with various response
formats. Run this script when you have the necessary API credentials
set.
"""

import os
import json
import sys


def main():
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    from receipt_ocr.processors import ReceiptProcessor

    processor = ReceiptProcessor()

    # Simple schema for json_object and text formats
    simple_json_schema = {
        "merchant_name": "string",
        "merchant_address": "string",
        "transaction_date": "string",
        "transaction_time": "string",
        "total_amount": "number",
        "line_items": [
            {
                "item_name": "string",
                "item_quantity": "number",
                "item_price": "number",
            }
        ],
    }

    # Proper JSON Schema for OpenAI json_schema format
    openai_json_schema = {
        "type": "object",
        "properties": {
            "merchant_name": {"type": "string"},
            "merchant_address": {"type": "string"},
            "transaction_date": {"type": "string"},
            "transaction_time": {"type": "string"},
            "total_amount": {"type": "number"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "item_name": {"type": "string"},
                        "item_quantity": {"type": "number"},
                        "item_price": {"type": "number"},
                    },
                    "required": ["item_name", "item_quantity", "item_price"],
                    "additionalProperties": False,
                },
            },
        },
        "required": [
            "merchant_name",
            "merchant_address",
            "transaction_date",
            "transaction_time",
            "total_amount",
            "line_items",
        ],
        "additionalProperties": False,
    }

    # Test all response format types
    results = {}
    results["json_object"] = processor.process_receipt(
        "images/receipt.jpg",
        simple_json_schema,
        response_format_type="json_object",
    )
    results["json_schema"] = processor.process_receipt(
        "images/receipt.jpg",
        openai_json_schema,
        response_format_type="json_schema",
    )
    results["text"] = processor.process_receipt(
        "images/receipt.jpg", simple_json_schema, response_format_type="text"
    )

    # Validate all results
    all_passed = True
    for format_type, result in results.items():
        if result and isinstance(result, dict) and "merchant_name" in result:
            print(f"{format_type.upper()} test passed: structured data extracted")
            print(f"Sample output: {json.dumps(result, indent=2)}")
        else:
            print(
                f"{format_type.upper()} test failed: invalid or missing structured data"
            )
            print(f"Result: {result}")
            all_passed = False

    if all_passed:
        print("All programmatic tests passed")
        sys.exit(0)
    else:
        print("Some programmatic tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
