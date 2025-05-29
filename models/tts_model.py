"""
Text-to-Speech (TTS) Module

Uses Microsoft Edge TTS service to convert text to natural-sounding speech.
Implements async operations for better performance.
"""

import edge_tts
import asyncio

async def generate_speech(text, path):
    """
    Generate speech from text using Edge TTS.
    
    Args:
        text (str): Text to convert to speech
        path (str): Output path for the generated audio file
        
    Notes:
        Uses zh-CN-XiaoxiaoNeural voice model for consistent character voice
    """
    communicate = edge_tts.Communicate(text=text, voice="zh-CN-XiaoxiaoNeural")
    await communicate.save(path)
