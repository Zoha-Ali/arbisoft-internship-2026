import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")

response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    },
    json={
        "model": "claude-sonnet-5",
        "max_tokens": 100,
        "messages": [
            {"role": "user", "content": "Say hello in one short sentence."}
        ],
    },
)

print(response.json())