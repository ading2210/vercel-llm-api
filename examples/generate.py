import vercel_ai
import logging
import json
import random

vercel_ai.logger.setLevel(logging.INFO)

client = vercel_ai.Client()
for chunk in client.generate(f"Summarize the GNU GPL v3. {random.randint(0, 1000)}"):
  print(chunk, end="", flush=True)
print()