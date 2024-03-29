.. LanguageAssistant documentation master file, created by
   sphinx-quickstart on Mon Jun 12 11:46:40 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LanguageAssistant Documentation
=============================================

| **LanguageAssistant** is a large language model (LLM) powered assistant for learning foreign languages organically.

The goal of LanguageAssistant is to harness the incredible multi-lingual conversation capabilities of modern
chat LLMs using `LangChain <https://github.com/hwchase17/langchain>`_ to provide a seamless language learning
experience comparable to paid professional language tutors.

Whether starting from scratch or looking to hone your language skills through real-world conversations,
LanguageAssistant can help through its real-time transcription (powered by
`OpenAI's Whisper <https://openai.com/research/whisper>`_) and multi-lingual text-to-speech (powered by
`Google TTS <https://cloud.google.com/text-to-speech>`_).

This project is largely a proof of concept, but has been setup to be extensible so that it could be used as a
backend for a full-fledged application utilizing a better UI, microphone recording, transcription, LLM prompts,
and/or multi-lingual text-to-speech.

Features of LanguageAssistant:

   - Full real-time vocal multilingual conversations
   - Real-time voice transcription
   - LLM text responses
   - Multilingual text-to-speech
   - LLM agent for lesson planning


.. toctree::
   :maxdepth: 1
   :caption: Getting Started
   :hidden:

   User Guide <getting_started/user_guide>
   Contributing Guide <getting_started/contributing>
   Full Example <getting_started/full_conversation_example>

.. toctree::
   :caption: API Reference
   :hidden:

   API Reference <reference>

.. toctree::
   :maxdepth: 1
   :caption: Extras
   :hidden:

   Changelog <changelog>
