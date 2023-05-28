#import requests
import logging
import re
import json
import base64
import quickjs
import tls_client as requests

logging.basicConfig()
logger = logging.getLogger()

class Client:
  base_url = "https://play.vercel.ai"
  token_url = base_url + "/openai.jpeg" #nice try vercel
  generate_url = base_url + "/api/generate"

  def __init__(self):
    self.session = requests.Session(client_identifier="chrome_113")
    self.headers = {
      "Accept": "*/*",
      "Accept-Language": "en-US,en;q=0.9,und;q=0.8,af;q=0.7",
      "Sec-Ch-Ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
      "Sec-Ch-Ua-Mobile": "?0",
      "Sec-Ch-Ua-Platform": '"Chrome OS"',
      "Sec-Gpc": "1",
      "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    self.session.headers.update(self.headers)

    self.models = self.get_models()

  def get_models(self):
    logger.info("Downloading homepage...")
    html = self.session.get(self.base_url).text
    paths_regex = r'static\/chunks.+?\.js'
    separator_regex = r'"\]\)<\/script><script>self\.__next_f\.push\(\[.,"'

    paths = re.findall(paths_regex, html)
    for i in range(len(paths)):
      paths[i] = re.sub(separator_regex, "", paths[i])
    paths = list(set(paths))

    for path in paths:
      script_url = f"{self.base_url}/_next/{path}"
      logger.info(f"Downloading and parsing {script_url}...")

      script = self.session.get(script_url).text
      models_regex = r'let .="\\n\\nHuman:\",r=(.+?),.='
      matches = re.findall(models_regex, script)

      if matches:
        models_str = matches[0]
        stop_sequences_regex = r'(?<=stopSequences:{value:\[)\D(?<!\])'
        models_str = re.sub(stop_sequences_regex, re.escape('"\\n\\nHuman:"'), models_str)

        context = quickjs.Context()
        return context.eval(f"({models_str})").json()
    
    return []

  def get_token(self):
    logger.info("Fetching token from "+self.token_url)
    b64 = self.session.get(self.token_url).text
    data = json.loads(base64.b64decode(b64))

    script = """
      var globalThis = {{data: "sentinel"}};
      ({script})({key})
    """.format(script=data["c"], key=data["a"])
    
    context = quickjs.Context()
    token_data = json.loads(context.eval(script).json())
    token = {
      "r": token_data,
      "t": data["t"]
    }
    token_string = json.dumps(token, separators=(',', ':')).encode()
    return base64.b64encode(token_string).decode()

  def generate(self, prompt, **kwargs):
    logger.info(f"Sending {prompt}")
    token = self.get_token()
    payload = {
      "prompt": prompt,
      "model": "openai:gpt-3.5-turbo",
      "temperature": 0.7,
      "maxTokens": 200,
      "topK": 1,
      "topP": 1,
      "frequencyPenalty": 1,
      "presencePenalty": 1,
      "stopSequences": []
    }
    headers = {**self.headers, **{
      "Accept-Encoding": "gzip, deflate, br",
      "Custom-Encoding": token,
      "Host": "play.vercel.ai",
      "Origin": "https://play.vercel.ai",
      "Referrer": "https://play.vercel.ai",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",
    }}

    logger.info(f"Waiting for server response")
    response = self.session.post(self.generate_url, json=payload, headers=headers)
    
    
    output = ""
    for line in response.text.split("\n"):
      if line:
        output += json.loads(line)
    return output
    
    """
    response = self.session.post(self.generate_url, json=payload, headers=headers, stream=True)
    
    for chunk in response.iter_content(chunk_size=None):
      yield chunk
      response.raise_for_status()"""