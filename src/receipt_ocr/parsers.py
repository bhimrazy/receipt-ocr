import json


class ReceiptParser:
    """Parser for the LLM's response."""

    def parse(self, response: str) -> dict:
        """Parse the LLM's response and return a JSON object."""
        try:
            # The response is often wrapped in a code block
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:-4]
            elif response.startswith("```"):
                response = response[3:-3]
            return json.loads(response)
        except json.JSONDecodeError:
            # Handle the case where the response is not valid JSON
            return {"error": "The LLM's response was not valid JSON."}
