# User Setup Guide


## Installation

```shell
pip install languageassistant
```

## Configure API keys

There are two environment variables that must be configured
for LanguageAssistant to fully work. For development, you may choose
to just use a .env file with
[python-dotenv](https://pypi.org/project/python-dotenv/).

If you have cloned the repo for developing LanguageAssistant, it already uses
the [Poetry dotenv plugin](https://pypi.org/project/poetry-dotenv-plugin/)
to use a local .env file.

Necessary environment variables:
1. `OPENAI_API_KEY`: OpenAI's API key to use for Whisper audio transcription
2. `GOOGLE_API_KEY`: Google's Text-to-Speech API key

### OpenAI

1. Login or create an new [OpenAI](https://platform.openai.com/account/api-keys)
account
2. Click the `Create new secret key` button
3. Copy that API key and export the `OPENAI_API_KEY`
 environment variable with the API key as its value

### Google Cloud

Setting up Google Cloud takes a bit more work of navigating menus.

1. Login to Google at https://console.cloud.google.com/
2. Click `Select a project`
3. Create a new project
4. Select the newly created project as your active project
5. Enable the
[Cloud Text-to-Speech API](https://console.cloud.google.com/marketplace/product/google/texttospeech.googleapis.com)
6. Return to the console and click `Credentials`
7. Click `Create Credentials` -> `API Key`
8. Copy and export the `GOOGLE_API_KEY` environment variable with the API
key as its value


## Run the assistant

Download the demo from https://github.com/dagleaves/languageassistant/blob/main/main.py

```shell
python main.py
```
