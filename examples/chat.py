import vercel_ai
import logging
import json
import random

vercel_ai.logger.setLevel(logging.INFO)
client = vercel_ai.Client()

messages = [
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "Who won the world series in 2020?"},
  {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
  {"role": "user", "content": "Where was it played?"}
]
params = {
  "maxTokens": 600
}

for chunk in client.chat("openai:gpt-3.5-turbo", messages, params=params):
  print(chunk, end="", flush=True)
print()