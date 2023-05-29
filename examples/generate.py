import vercel_ai
import logging
import json
import random

vercel_ai.logger.setLevel(logging.INFO)
client = vercel_ai.Client()

prompt = f"Summarize the GNU GPL v3 in 3 paragraphs. {random.randint(0, 1000)}"
params = {
  "maximumLength": 1000
}

for chunk in client.generate("openai:gpt-3.5-turbo", prompt, params=params):
  print(chunk, end="", flush=True)
print()