"""
Automatic Speech Recognition (ASR) Module

Uses OpenAI's Whisper model to convert speech to text.
Supports multiple audio formats and languages.
"""

import whisper

# Initialize Whisper model with base configuration
model = whisper.load_model("base")

def transcribe_audio(file_path):
    """
    Transcribe audio file to text using Whisper ASR.
    
    Args:
        file_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text, stripped of leading/trailing whitespace
    """
    result = model.transcribe(file_path)
    return result["text"].strip()