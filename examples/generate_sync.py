import vercel_ai
import logging
import random

vercel_ai.logger.setLevel(logging.INFO)
client = vercel_ai.Client(proxy=True)

prompt = "What is git?" + " "*random.randint(0, 200)
params = {
  "maximumLength": 1000
}

response = client.generate_sync("openai:gpt-3.5-turbo", prompt, params=params)
print(response.text)