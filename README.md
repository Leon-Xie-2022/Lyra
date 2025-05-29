# 🧠 Lyra: Multimodal AI Assistant

**Lyra** is an intelligent assistant that supports **both voice and text-based interaction**.
It integrates **OpenAI Whisper** for speech recognition, **DeepSeek Chat API** for conversational generation, and **Microsoft Edge TTS** for voice synthesis—designed to deliver a smooth and natural dialogue experience.

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Leon-Xie-2022/Lyra.git
cd Lyra
```

### 2. Create the Environment

Make sure you have [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed.

```bash
conda env create -f environment.yml
conda activate lyra
```

### 3. Set Up DeepSeek API Key

Create a `.env` file in the project root and add your API key:

```plaintext
DEEPSEEK_API_KEY=your_api_key_here
```

### 4. Launch the Application

```bash
python web_app.py
```

Then visit [http://127.0.0.1:5000](http://127.0.0.1:5000) to start chatting.

---

## 💡 Key Features

* **Multimodal Interaction**

  * Supports both text and voice input
  * **Intelligently selects between text or voice output based on context**
  * Voice messages can be played and transcribed to text

* **Personalization**

  * Configurable user preferences
  * Adjustable output mode (text/voice)
  * User profile and settings

* **Emotional Intelligence** (in development)

  * Emotion-aware dialogue generation
  * Real-time emotion display
  * Context-sensitive interaction

---

## 📍 Project Structure

```
lyra/
├── web_app.py              # Flask application entry point
├── environment.yml         # Conda environment configuration
├── history.txt             # Conversation history
├── README.md               # English documentation
├── README_zh.md            # Chinese documentation
│
├── models/                 # Core functional modules
│   ├── asr_model.py        # ASR module (Whisper)
│   ├── chat_model.py       # Chat API interface (DeepSeek)
│   └── tts_model.py        # Text-to-Speech module (Edge TTS)
│
├── static/                 # Static resources
│   ├── audio/              # Audio file storage
│   ├── css/
│   │   └── style.css       # Application styles
│   └── js/
│       └── main.js         # Front-end logic
│
└── templates/              # HTML templates
    └── index.html          # Main interface
```

---

## 🛠️ Development Notes

### Backend Modules

#### Main App (`web_app.py`)

The Flask backend handles routing and API services:

* `POST /api/chat`

  * Processes user messages and generates AI responses
  * Input: message, user preferences
  * Output: text/audio reply, emotional state, audio URL (if applicable)

* `POST /api/speech-to-text`

  * Converts audio input (WebM) to text
  * Output: transcribed content

* `GET /api/get-memory`

  * Retrieves historical conversation records
  * Output: ordered dialogue list

#### Model Modules (`models/`)

* `asr_model.py`: Speech recognition via Whisper, supports multilingual input
* `chat_model.py`: Handles DeepSeek conversation API with context and emotion
* `tts_model.py`: Voice synthesis using Edge TTS with natural speech output

### Frontend Structure

#### Static Assets (`static/`)

* `js/main.js`: Main front-end logic

  * Voice recording/playback
  * WebSocket management
  * UI state and animations
  * Message exchange handling
* `css/style.css`: Responsive layout and visual theme
* `audio/`: Temporary audio storage

  * Stores user inputs (WebM)
  * Stores AI voice replies (WAV)

#### Templates (`templates/`)

* `index.html`: Main UI with chat interface and settings panel

---

## 📢 Disclaimer

**Lyra** is an experimental open-source project designed to explore early-stage multimodal interaction.
You are welcome to customize and expand it according to your needs.