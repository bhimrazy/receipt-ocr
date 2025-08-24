import os
from abc import ABC, abstractmethod
from openai import OpenAI
from PIL import Image
import base64
import io
from receipt_ocr.prompts import SYSTEM_PROMPT, USER_PROMPT


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    """

    @abstractmethod
    def get_response(self, image_path: str, json_schema: dict, model: str) -> str:
        """
        Get the response from the LLM provider.
        """
        pass


class OpenAIProvider(LLMProvider):
    """
    LLM provider for OpenAI-compatible APIs.
    """

    def __init__(self, api_key: str = None, base_url: str = None):
        """
        Initialize the OpenAI provider.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def get_response(self, image_path: str, json_schema: dict, model: str) -> str:
        """
        Get the response from the OpenAI API.
        """
        # Load the image
        image = Image.open(image_path)

        # Convert the image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Create the system prompt
        system_prompt = SYSTEM_PROMPT

        response = self.client.chat.completions.create(
            model=model,
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

        return response.choices[0].message.content
