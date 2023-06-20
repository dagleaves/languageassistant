import questionary

from languageassistant.assistant import Assistant
from languageassistant.transcriber import Transcriber
from languageassistant.tts import TTS
from languageassistant.utils import supported_languages


def custom_topics_loop(assistant: Assistant, include_background: bool) -> None:
    """Allow user to manually input each conversation topic"""
    while True:
        topic = questionary.text("What topic would you like to discuss?").ask()
        assistant.run(include_topic_background=include_background, lesson=[topic])

        # Continue with another topic?
        topic_backgrounds = questionary.select(
            "Would you like to start a new conversation?",
            choices=["Yes", "No"],
        ).ask()
        if topic_backgrounds == "No":
            return


def main() -> None:
    # Get user background information
    language = questionary.select(
        "What language would you like to learn?",
        choices=supported_languages,
    ).ask()
    proficiency = questionary.select(
        "What is your proficiency with this language?",
        choices=["Beginner", "Elementary", "Intermediate", "Advanced", "Fluent"],
    ).ask()

    # Include topic background instruction?
    topic_backgrounds = questionary.select(
        "Do you want to receive a lesson on the topics before starting the conversations?",
        choices=["Yes", "No"],
    ).ask()
    include_background = topic_backgrounds == "Yes"

    # Initialize models
    transcriber = Transcriber()
    tts = TTS(language=language)
    assistant = Assistant(
        language=language, proficiency=proficiency, transcriber=transcriber, tts=tts
    )

    # Does user want the assistant to come up with conversation topics?
    topic_backgrounds = questionary.select(
        "Do you want the assistant to generate conversation topics?",
        choices=["Yes", "No, I want to manually enter them myself"],
    ).ask()
    if topic_backgrounds == "Yes":
        assistant.run(include_topic_background=include_background)
    else:
        custom_topics_loop(assistant, include_background)


if __name__ == "__main__":
    main()
