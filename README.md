# Python Vercel LLM API

[![PyPi Version](https://img.shields.io/pypi/v/vercel-llm-api.svg)](https://pypi.org/project/vercel-llm-api/)

This is a reverse engineered API wrapper for the [Vercel AI Playground](https://play.vercel.ai/), which allows for free access to many LLMs, including OpenAI's ChatGPT, Cohere's Command Nightly, as well as some open source models.

## Table of Contents:
- [Features](#features)
- [Limitations](#limitations)
- [Installation](#installation)
- [Documentation](#documentation)
  * [Using the Client](#using-the-client)
    + [Downloading the Available Models](#downloading-the-available-models)
    + [Generating Text](#generating-text)
    + [Generating Chat Messages](#generating-chat-messages)
  * [Misc](#misc)
    + [Changing the Logging Level](#changing-the-logging-level)
- [Copyright](#copyright)
  * [Copyright Notice](#copyright-notice)

*Table of contents generated with [markdown-toc](http://ecotrust-canada.github.io/markdown-toc).*

## Features:
 - Download the available models
 - Generate text
 - Generate chat messages
 - Set custom parameters
 - Stream the responses

## Limitations:
 - User-agent is hardcoded
 - No auth support
 - Can't use "pro" or "hobby" models

## Installation:
You can install this library by running the following command:
```
pip3 install vercel-llm-api
```

## Documentation:
Examples can be found in the `/examples` directory. To run these examples, simply execute the included Python files from your terminal.
```
python3 examples/generate.py
```

### Using the Client:
To use this library, simply import `vercel_ai` and create a `vercel_ai.Client` instance. You can specify a proxy using the `proxy` keyword argument.

Normal example:
```python
import vercel_ai
client = vercel_ai.Client()
```

Proxied example:
```python
import vercel_ai
client = vercel_ai.Client(proxy="socks5h://193.29.62.48:11003")
```

Note that the following examples assume `client` is the name of your `vercel_ai.Client` instance.

#### Downloading the Available Models:
The client downloads the available models upon initialization, and stores them in `client.models`. 
```python
>>> print(json.dumps(client.models, indent=2))

{
  "anthropic:claude-instant-v1": { 
    "id": "anthropic:claude-instant-v1", #the model's id
    "provider": "anthropic",             #the model's provider
    "providerHumanName": "Anthropic",    #the provider's display name
    "makerHumanName": "Anthropic",       #the maker of the model
    "minBillingTier": "hobby",           #the minimum billing tier needed to use the model
    "parameters": {                      #a dict of optional parameters that can be passed to the generate function
      "temperature": {                   #the name of the parameter
        "value": 1,                      #the default value for the parameter
        "range": [0, 1]                  #a range of possible values for the parameter
      },
      ...
    }
    ...
  }
}
```
Note that, since there is no auth yet, if a model has the `"minBillingTier"` property present, it can't be used.

A list of model IDs is also available in `client.model_ids`.
```python
>>> print(json.dumps(client.model_ids, indent=2))
[
  "anthropic:claude-instant-v1", #locked to hobby tier; unusable
  "anthropic:claude-v1",         #locked to hobby tier; unusable
  "replicate:replicate/alpaca-7b",
  "replicate:stability-ai/stablelm-tuned-alpha-7b",
  "huggingface:bigscience/bloom",
  "huggingface:bigscience/bloomz",
  "huggingface:google/flan-t5-xxl",
  "huggingface:google/flan-ul2",
  "huggingface:EleutherAI/gpt-neox-20b",
  "huggingface:OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
  "huggingface:bigcode/santacoder",
  "cohere:command-medium-nightly",
  "cohere:command-xlarge-nightly",
  "openai:gpt-4",                #locked to pro tier; unusable
  "openai:code-cushman-001",
  "openai:code-davinci-002",
  "openai:gpt-3.5-turbo",
  "openai:text-ada-001",
  "openai:text-babbage-001",
  "openai:text-curie-001",
  "openai:text-davinci-002",
  "openai:text-davinci-003"
]
```

A dict of default parameters for each model can be found at `client.model_params`.
```python
>>> print(json.dumps(client.model_defaults, indent=2))
{
  "anthropic:claude-instant-v1": {
    "temperature": 1,
    "maximumLength": 200,
    "topP": 1,
    "topK": 1,
    "presencePenalty": 1,
    "frequencyPenalty": 1,
    "stopSequences": [
      "\n\nHuman:"
    ]
  },
  ...
}
```

#### Generating Text:
To generate some text, use the `client.generate` function, which accepts the following arguments:
 - `model` - The ID of the model you want to use.
 - `prompt` - Your prompt.
 - `params = {}` - A dict of optional parameters. See the previous section for how to find these.

The function is a generator which returns the newly generated text as a string.

Streamed Example:
```python
for chunk in client.generate("openai:gpt-3.5-turbo", "Summarize the GNU GPL v3"):
  print(chunk, end="", flush=True)
```

Non-Streamed Example:
```python
result = ""
for chunk in client.generate("openai:gpt-3.5-turbo", "Summarize the GNU GPL v3"):
  result += chunk
print(result)
```

#### Generating Chat Messages:
To generate chat messages, use the `client.chat` function, which accepts the following arguments:
 - `model` - The ID of the model you want to use.
 - `messages` - A list of messages. The format for this is identical to how you would use the official OpenAI API.
 - `params = {}` - A dict of optional parameters. See the "Downloading the Available Models" section for how to find these.

The function is a generator which returns the newly generated text as a string.

```python
messages = [
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "Who won the world series in 2020?"},
  {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
  {"role": "user", "content": "Where was it played?"}
]
for chunk in client.chat("openai:gpt-3.5-turbo", messages):
  print(chunk, end="", flush=True)
print()
```

### Misc:

#### Changing the Logging Level:
If you want to show the debug messages, simply call `vercel_ai.logger.setLevel`.

```python
import vercel_ai
import logging
vercel_ai.logger.setLevel(logging.INFO)
```

## Copyright:
This program is licensed under the [GNU GPL v3](https://github.com/ading2210/vercel-llm-api/blob/main/LICENSE). All code has been written by me, [ading2210](https://github.com/ading2210).

### Copyright Notice:
```
ading2210/vercel-llm-api: a reverse engineered API wrapper for the Vercel AI Playground
Copyright (C) 2023 ading2210

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```