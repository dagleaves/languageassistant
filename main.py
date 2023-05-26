import questionary

from languageassistant.assistant import Assistant
from languageassistant.transcriber import Transcriber


def main() -> None:
    language = questionary.select(
        "What language would you like to learn?",
        choices=["English", "Spanish", "Chinese"],
    ).ask()
    proficiency = questionary.select(
        "What is your proficiency with this language?",
        choices=["Beginner", "Elementary", "Intermediate", "Advanced", "Fluent"],
    ).ask()
    transcriber = Transcriber()
    assistant = Assistant(
        language=language, proficiency=proficiency, transcriber=transcriber
    )
    assistant.run()


if __name__ == "__main__":
    main()
