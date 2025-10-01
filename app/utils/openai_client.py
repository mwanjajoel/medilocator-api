import openai
import os
from typing import List, Dict
from app.core.config import settings

class OpenAIClient:
    def __init__(self):
        openai.api_key = settings.openai_api_key
        if not openai.api_key:
            raise ValueError("OpenAI API key not configured")

    async def chat_completion(self, messages: List[Dict]) -> str:
        """Make call to OpenAI Chat Completion API"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.1,
                max_tokens=200,
                timeout=30
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            print(f"OpenAI API error: {e}")
            raise Exception("OpenAI service unavailable")

# Global OpenAI client instance
openai_client = OpenAIClient()