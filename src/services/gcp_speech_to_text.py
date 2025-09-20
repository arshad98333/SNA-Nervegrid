from google.cloud import speech

def transcribe_audio(audio_content: bytes, language_code: str = "en-IN") -> str:
    """
    Transcribes audio content using Google Cloud Speech-to-Text API.

    Args:
        audio_content (bytes): The raw byte content of the audio file.
        language_code (str): The language code (e.g., "en-IN", "hi-IN").

    Returns:
        str: The transcribed text or a formatted error/warning message.
    """
    try:
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            language_code=language_code,
            enable_automatic_punctuation=True
        )
        response = client.recognize(config=config, audio=audio)

        transcript = "".join(result.alternatives[0].transcript for result in response.results)
        
        if not transcript:
            return "Warning: Audio processed, but no speech was recognized."
        
        print(f"[INFO] Speech-to-Text transcription successful for '{language_code}'.")
        return transcript
    except Exception as e:
        error_message = f"Error transcribing audio. Check API is enabled and audio format is supported. Details: {e}"
        print(f"[ERROR] {error_message}")
        return error_message