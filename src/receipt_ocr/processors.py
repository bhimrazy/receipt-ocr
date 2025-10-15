from typing import Any, Dict, Optional

from receipt_ocr.parsers import ReceiptParser
from receipt_ocr.providers import OpenAIProvider


class ReceiptProcessor:
    """Process a receipt image and return a structured JSON object."""

    def __init__(
        self,
        provider: Optional[OpenAIProvider] = None,
        parser: Optional[ReceiptParser] = None,
    ):
        """Initialize the receipt processor."""
        self.provider = provider or OpenAIProvider()
        self.parser = parser or ReceiptParser()

    def process_receipt(
        self,
        image_path: str,
        json_schema: Dict[str, Any],
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process a receipt image and return a structured JSON object."""
        response = self.provider.get_response(image_path, json_schema, model)
        content = response.choices[0].message.content
        return self.parser.parse(content)
