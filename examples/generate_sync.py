import vercel_ai
import logging
import random

vercel_ai.logger.setLevel(logging.INFO)
client = vercel_ai.Client(proxy=True)
model = "openai:gpt-3.5-turbo-16k-0613"
params = { "maximumLength": 1000 }
prompt = "What is git?" + " "*random.randint(0, 200)
done = False

while not done:
  try:
    response = client.generate_sync("openai:gpt-3.5-turbo", prompt, params=params)
    done = True
  except RuntimeError as e:
    client = vercel_ai.Client()


print(response.text)