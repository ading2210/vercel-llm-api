import vercel_ai
import logging

#list the available models

vercel_ai.logger.setLevel(logging.INFO)
client = vercel_ai.Client()
print(client.model_ids)