import argparse
import os
import json
from receipt_ocr.providers import OpenAIProvider
from receipt_ocr.parsers import ReceiptParser
from dotenv import load_dotenv

load_dotenv()


class ReceiptProcessor:
    """
    Process a receipt image and return a structured JSON object.
    """

    def __init__(self, provider, parser):
        """
        Initialize the receipt processor.
        """
        self.provider = provider
        self.parser = parser

    def process_receipt(self, image_path: str, json_schema: dict, model: str) -> dict:
        """
        Process a receipt image and return a structured JSON object.
        """
        response = self.provider.get_response(image_path, json_schema, model)
        return self.parser.parse(response)


def main():
    """
    Main function for the CLI.
    """
    parser = argparse.ArgumentParser(
        description="Extract information from a receipt image."
    )
    parser.add_argument("image_path", type=str, help="The path to the receipt image.")
    parser.add_argument(
        "--schema_path", type=str, help="The path to a custom JSON schema file."
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("OPENAI_MODEL", "gpt-4.1"),
        help="The model to use for the LLM.",
    )
    parser.add_argument("--api_key", type=str, help="The API key for the LLM provider.")
    parser.add_argument(
        "--base_url", type=str, help="The base URL for the LLM provider."
    )
    args = parser.parse_args()

    # Load the JSON schema
    if args.schema_path:
        with open(args.schema_path, "r") as f:
            json_schema = json.load(f)
    else:
        json_schema = {
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

    # Initialize the provider and parser
    provider = OpenAIProvider(api_key=args.api_key, base_url=args.base_url)
    parser = ReceiptParser()

    # Initialize the processor
    processor = ReceiptProcessor(provider, parser)

    # Process the receipt
    result = processor.process_receipt(args.image_path, json_schema, args.model)

    # Print the result
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
