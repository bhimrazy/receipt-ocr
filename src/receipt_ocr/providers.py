import json
import os
from abc import ABC, abstractmethod
from typing import Any, Optional, Union

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from PIL import Image

from receipt_ocr.constants import _DEFAULT_OPENAI_MODEL
from receipt_ocr.prompts import SYSTEM_PROMPT, USER_PROMPT
from receipt_ocr.utils import encode_image_to_base64


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def get_response(
        self, image: Union[str, bytes, Image.Image], json_schema: dict, model: str
    ) -> Any:
        """Get the response from the LLM provider."""
        pass


class OpenAIProvider(LLMProvider):
    """LLM provider for OpenAI-compatible APIs."""

    def __init__(self, api_key: str = None, base_url: str = None):
        """Initialize the OpenAI provider."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def get_response(
        self,
        image: Union[str, bytes, Image.Image],
        json_schema: dict,
        model: Optional[str] = None,
    ) -> ChatCompletion:
        """Get the response from the OpenAI API."""
        # Encode image to base64 using utility function
        img_str = encode_image_to_base64(image)

        # Create the system prompt
        system_prompt = SYSTEM_PROMPT.format(
            json_schema_content=json.dumps(json_schema, indent=2)
        )

        response = self.client.chat.completions.create(
            model=model or os.getenv("OPENAI_MODEL", _DEFAULT_OPENAI_MODEL),
            response_format={"type": "json_object"},
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": USER_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_str}"},
                        },
                    ],
                },
            ],
        )

        return response
