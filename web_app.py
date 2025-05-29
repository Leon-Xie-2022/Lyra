"""
A Flask web application for the Lyra chat system that handles:
- Text and voice-based chat interactions
- Speech-to-text and text-to-speech conversion
- Chat history management
- Audio file handling
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import uuid
import asyncio
import json
from datetime import datetime
from models.asr_model import transcribe_audio
from models.chat_model import generate_reply
from models.tts_model import generate_speech

# Configuration constants
HISTORY_FILE = "history.txt"
UPLOAD_FOLDER = "static/audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def save_message(role, content, emotion="calm", output_type="text", audio_filename=None):
    """
    Save a chat message to the history file.
    
    Args:
        role (str): The role of the message sender ('user' or 'lyra')
        content (str): The text content of the message
        emotion (str, optional): The emotional state. Defaults to 'calm'
        output_type (str, optional): Type of output ('text' or 'voice'). Defaults to 'text'
        audio_filename (str, optional): Name of the associated audio file. Defaults to None
        
    Note:
        Messages are stored in JSON format with timestamp and optional audio URL
    """
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "emotion": emotion,
        "output_type": output_type
    }

    if output_type == "voice" and audio_filename:
        message["audio_url"] = f"/audio/{audio_filename}"

    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(message, ensure_ascii=False) + "\n")

@app.route("/")
def index():
    """Serve the main chat interface."""
    return render_template("index.html")

@app.route("/audio/<path:filename>")
def audio(filename):
    """Serve audio files from the upload folder."""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Handle chat messages and generate responses.
    
    Accepts POST requests with JSON body containing:
    - message: User's text input
    - is_voice: Boolean indicating if input is from voice transcription
    
    Returns JSON response with:
    - message: AI response text
    - output_type: 'text' or 'voice'
    - audio_url: URL to audio file (for voice responses)
    - emotion: AI's emotional state
    """
    data = request.json
    user_input = data.get("message", "")
    is_voice_input = data.get("is_voice", False)

    if not is_voice_input:
        save_message("user", user_input)

    # Initialize conversation history
    messages = []

    # Load conversation history
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    entry = json.loads(line.strip())
                    role = entry["role"]
                    
                    # Convert 'lyra' role to 'assistant' for model compatibility
                    if role == "lyra":
                        role = "assistant"
                        
                    messages.append({
                        "role": role,
                        "content": entry["content"],
                        "emotion": entry.get("emotion", "neutral"),
                        "output_type": entry.get("output_type", "text")
                    })
        except Exception as e:
            print("[ERROR] Failed to load history:", e)

    # Add current user input to conversation
    messages.append({"role": "user", "content": user_input})

    # Generate AI response using the language model
    try:
        result = generate_reply(messages)
        answer = result.get("content", "I apologize, I cannot respond at the moment.")
        emotion = result.get("emotion", "neutral")
        output_type = result.get("output_type", "text")

    # Handle LLM errors with a friendly default response
    except Exception as e:
        print("[LLM ERROR]", e)
        answer = "I'm sorry, I didn't quite catch that."

    # Add the AI response to the conversation history
    messages.append({"role": "assistant", "content": answer})

    audio_file = None
    # Handle voice output if selected by the model
    if output_type == "voice":
        # Generate unique filename for the audio response
        audio_file = f"reply_{uuid.uuid4()}.wav"
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file)
        
        # Asynchronously generate speech from text
        try:
            asyncio.run(generate_speech(answer, audio_path))
        except Exception as e:
            print("[ERROR] TTS failed:", e)
            audio_file = None    
            
        # Save response with audio file reference
        save_message("lyra", answer, emotion, output_type, audio_file)
    else:
        # Save text-only response
        save_message("lyra", answer, emotion, output_type)
    
    # Return response with message content, output type, audio URL if available, and emotional state
    return jsonify({
        "message": answer,
        "output_type": output_type,
        "audio_url": f"/audio/{audio_file}" if audio_file else None,
        "emotion": emotion
    })
@app.route("/api/speech-to-text", methods=["POST"])
def speech_to_text():
    """
    Convert uploaded audio to text using ASR.
    
    Accepts:
        POST request with audio file in FormData
        
    Returns:
        JSON with:
        - text: Transcribed text from the audio
        - file: Name of the saved audio file
        
    Raises:
        400: If no audio file is provided
        500: If ASR processing fails
    """
    uploaded_file = request.files.get('audio')
    if not uploaded_file:
        return jsonify({'error': 'No audio file provided'}), 400

    filename = f"input_{uuid.uuid4().hex}.webm"
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(saved_path)

    try:
        text = transcribe_audio(saved_path)
        save_message("user", text, output_type="voice", audio_filename=filename)
        return jsonify({"text": text, "file": filename})
    except Exception as e:
        print("[ASR ERROR]", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/get-memory", methods=["GET"])
def get_memory():
    """
    Retrieve chat history from the history file.
    
    Returns:
        JSON array of messages, each containing:
        - role: Message sender ('user' or 'lyra')
        - content: Message text
        - timestamp: ISO format timestamp
        - emotion: Emotional state
        - output_type: 'text' or 'voice'
        - audio_url: URL to audio file (for voice messages)
    """
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line.strip())
                history.append(entry)
    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True)