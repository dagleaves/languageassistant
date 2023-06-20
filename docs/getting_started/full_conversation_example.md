# LanguageAssistant Full Feature Demo

To run this example, see [examples/main.py](https://github.com/dagleaves/languageassistant/blob/main/examples/main.py)

```python
# Imports
from languageassistant.assistant import Assistant
from languageassistant.transcriber import Transcriber
from languageassistant.tts import TTS
```

Next, save your user information and settings. If you don't want the agent provide an
introductory lesson before starting the conversation, set `include_topic_lesson` to False.

```python
target_language = "Spanish"
proficiency = "Beginner"
include_topic_lesson = True
```

Initialize models using the user information and settings.

```python
# Initialize models
transcriber = Transcriber()
tts = TTS(language=target_language)
assistant = Assistant(
    language=target_language, proficiency=proficiency, transcriber=transcriber, tts=tts
)
```

Finally, run the assistant. If you would like the Assistant to come up with topics for you, run the following:

```python
assistant.run(include_topic_background=include_topic_lesson)
```

If you prefer to use your own topic(s), you can do provide your own via the `lesson` flag:

```python
topic = "Greetings and introductions"
assistant.run(include_topic_background=include_topic_lesson, lesson=[topic])
```
