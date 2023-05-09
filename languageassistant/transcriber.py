import io
import os
from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
from typing import Any, List, Optional

import openai
import speech_recognition as sr
from pydantic import BaseModel, Extra


def load_openai() -> None:
    try:
        import openai

        openai.api_key = os.getenv("OPENAI_API_KEY")
    except ImportError:
        raise ImportError(
            "Package `openai` is not installed"
            "Please install it with `pip install openai`"
        )


def print_transcription(transcription: List[str]) -> None:
    # Clear the console to reprint the updated transcription.
    os.system("cls" if os.name == "nt" else "clear")
    for line in transcription:
        print(line)
    # Flush stdout.
    print("", end="", flush=True)


def get_transcription(temp_file: str, wav_data: io.BytesIO) -> str:
    # Write wav data to the temporary file as bytes.
    with open(temp_file, "w+b") as wf:
        wf.write(wav_data.read())

    with open(temp_file, "rb") as rf:
        result = openai.Audio.transcribe("whisper-1", rf)
    text: str = result["text"].strip()
    return text


class Transcriber(BaseModel, extra=Extra.forbid):
    """Transcription model for user input."""

    record_timeout: Optional[float] = 2
    """How real-time the recording is."""
    phrase_timeout: Optional[float] = 3
    """Delay before ending user monologue"""
    energy_threshold: Optional[int] = 1000
    """Microphone """
    default_microphone: Optional[str] = "Microphone (2- Blue Snowball )"

    def get_microphone(self) -> sr.Microphone:
        """Get speech recognition microphone device"""
        mic_name = self.default_microphone

        # Allow user to pick microphone
        if not mic_name or mic_name == "list":
            print("Available microphone devices are: ")
            microphones = sr.Microphone.list_microphone_names()
            for index, name in enumerate(microphones):
                print(str(index + 1) + ". Microphone:", name)
            mic_idx = input(f"Select microphone number (1-{len(microphones)}): ")
            mic_name = microphones[int(mic_idx) - 1]

        # Get microphone object
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if mic_name in name:
                return sr.Microphone(sample_rate=16000, device_index=index)
        raise KeyError("No microphone with name", mic_name)

    def run(self) -> None:
        load_openai()
        # The last time a recording was retreived from the queue.
        phrase_time = None
        # Current raw audio bytes.
        last_sample = b""
        # Thread safe Queue for passing data from the threaded recording callback.
        data_queue = Queue()  # type: Queue
        # SpeechRecognizer to record because it can detect when speech ends.
        recorder = sr.Recognizer()
        recorder.energy_threshold = self.energy_threshold
        recorder.dynamic_energy_threshold = False
        record_timeout = self.record_timeout
        phrase_timeout = self.phrase_timeout

        temp_file = NamedTemporaryFile(suffix=".wav").name
        transcription = [""]

        def record_callback(_: Any, audio: sr.AudioData) -> None:
            """
            Threaded callback function to recieve audio data when recordings finish.
            audio: An AudioData containing the recorded bytes.
            """
            # Grab the raw bytes and push it into the thread safe queue.
            data = audio.get_raw_data()
            data_queue.put(data)

        with self.get_microphone() as source:
            recorder.adjust_for_ambient_noise(source)

        # Create a background thread that will pass us raw audio bytes.
        recorder.listen_in_background(
            source, record_callback, phrase_time_limit=record_timeout
        )
        print("Model loaded.\n")

        while True:
            try:
                now = datetime.utcnow()
                # Pull raw recorded audio from the queue.
                if not data_queue.empty():
                    phrase_complete = False
                    # If enough time has passed between recordings, consider the phrase complete.
                    # Clear the current working audio buffer to start over with the new data.
                    if phrase_time and now - phrase_time > timedelta(
                        seconds=phrase_timeout
                    ):
                        last_sample = b""
                        phrase_complete = True
                    # This is the last time we received new audio data from the queue.
                    phrase_time = now

                    # Concatenate our current audio data with the latest audio data.
                    while not data_queue.empty():
                        data = data_queue.get()
                        last_sample += data

                    # Use AudioData to convert the raw data to wav data.
                    audio_data = sr.AudioData(
                        last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH
                    )
                    wav_data = io.BytesIO(audio_data.get_wav_data())
                    text = get_transcription(temp_file, wav_data)

                    # If we detected a pause between recordings, add a new item to our transcripion.
                    # Otherwise edit the existing one.
                    if phrase_complete:
                        transcription.append(text)
                    else:
                        transcription[-1] = text

                    print_transcription(transcription)
                    sleep(0.25)
            except KeyboardInterrupt:
                break

        print("\n\nTranscription:")
        for line in transcription:
            print(line)


def main() -> None:
    transcriber = Transcriber()
    transcriber.run()


if __name__ == "__main__":
    main()
