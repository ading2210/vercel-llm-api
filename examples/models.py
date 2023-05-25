import vercel_ai
import logging
import json

vercel_ai.logger.setLevel(logging.INFO)

client = vercel_ai.Client()
print(json.dumps(client.models, indent=2))