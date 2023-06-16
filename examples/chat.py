import vercel_ai
import logging
import json
import random

vercel_ai.logger.setLevel(logging.INFO)
client = vercel_ai.Client()

messages = [
  {
    "content": f"test {random.randint(0, 1000)}",
    "role": "user"
  },
  {
    "content": "This is a test response from an AI language model. How may I assist you today?",
    "role": "assistant"
  },
  {
    "content": "summarize the gnu gpl v3",
    "role": "user"
  }
]
params = {
  "maxTokens": 600
}

for chunk in client.chat("openai:gpt-3.5-turbo", messages, params=params):
  print(chunk, end="", flush=True)
print()