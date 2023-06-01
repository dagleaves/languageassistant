import questionary

from languageassistant.assistant import Assistant
from languageassistant.transcriber import Transcriber
from languageassistant.tts import TTS
from languageassistant.utils import supported_languages


def main() -> None:
    language = questionary.select(
        "What language would you like to learn?",
        choices=supported_languages,
    ).ask()
    proficiency = questionary.select(
        "What is your proficiency with this language?",
        choices=["Beginner", "Elementary", "Intermediate", "Advanced", "Fluent"],
    ).ask()
    transcriber = Transcriber()
    tts = TTS(language=language)
    assistant = Assistant(
        language=language, proficiency=proficiency, transcriber=transcriber, tts=tts
    )
    assistant.run()


if __name__ == "__main__":
    main()
