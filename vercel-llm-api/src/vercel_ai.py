import requests
import logging
import re
import json
import chompjs

logging.basicConfig()
logger = logging.getLogger()

class Client:
  base_url = "https://play.vercel.ai"

  def __init__(self):
    self.session = requests.Session()
    self.headers = {
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
        return chompjs.parse_js_object(matches[0])
    
    return []