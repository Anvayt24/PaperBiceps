# 🎙️ PaperBiceps — AI-Powered Podcaster

<div align="center">
  <img src="paperbiceps_logo.jpg" alt="PaperBiceps Logo" width="300">
</div>

**Paper Biceps** is an AI tool that transforms any written content — research papers, articles, blogs, or documents — into realistic podcast conversations. It uses LLMs and TTS to simulate an actual podcast episode between a host and an expert.

---

## 🚀 Features

### v0.2.0 (Current)
- 🌐 **Chrome Extension** - Browser-based podcast generation with floating microphone
- 🔊 **Voice Explanations** - Smart query input for specific 'section' and 'Image' explanations ("Explain figure 1.2", "Read abstract")
- 🎧 **Built-in Audio Player** - With download functionality
- 🖱️ **Context Menu** - Right-click for quick podcast generation
- 🧠 **Gemini-powered** - Advanced summarization and script generation  
- 🎤 **Dynamic Dialogue** - Host-expert style Podcast conversations 
- 🗂️ **Multiple Input Formats** - PDF, TXT, DOCX, or URL
- 🎙️ **Dual-speaker Audio** - Using Deepgram TTS

### v0.1.0 (Legacy)
- 🧠 Gemini-powered summarization and script generation  
- 🎤 Dynamic host-expert style dialogue like a real podcast  
- 🗂️ Accepts PDF, TXT, DOCX, or URL input  
- 🎧 Dual-speaker audio generation using Deepgram TTS  
- 🎙️ Option to use Streamlit UI or FastAPI API  
- 🔊 Final podcast exported as an `.mp3`

---

## 🧰 Tech Stack

### Backend
- **Python 3.10+** - Core language
- **FastAPI** - Modern web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **HTTPX/Requests** - HTTP clients
- **Python-dotenv** - Environment management

### AI/ML Services
- **Google Gemini API** - LLM for script generation
- **Deepgram TTS** - Text-to-speech synthesis
- **spaCy** - Natural language processing

### Document Processing
- **PyMuPDF** - PDF text extraction
- **python-docx** - DOCX text extraction  
- **trafilatura** - Web content extraction

### Audio Processing
- **Pydub** - Audio manipulation

### Frontend
- **Chrome Extension** (Manifest v3)
- **Tailwind CSS** - Extension styling
- **JavaScript** - Extension logic

---

## 🏗️ Project Structure

```
PaperBiceps/
├── app/                          # Modular backend application
│   ├── main.py                   # FastAPI app entry point
│   ├── config.py                 # Configuration settings
│   ├── requirements.txt          # Python dependencies
│   ├── models/                   # Pydantic models
│   │   └── explain_request.py    # Request models
│   ├── routes/                   # API endpoints
│   │   ├── podcast.py            # Podcast generation endpoints
│   │   ├── explain.py            # Explanation endpoints
│   │   └── health.py             # Health check endpoints
│   ├── services/                 # Business logic
│   │   ├── gemini_service.py     # Gemini AI integration
│   │   ├── deepgram_service.py   # Deepgram TTS integration
│   │   └── scraping_service.py   # Web scraping service
│   └── utils/                    # Utility functions
│       ├── text_cleaning.py      # Text preprocessing
│       └── file_utils.py         # File handling utilities
├── extension/                    # Chrome extension
│   ├── manifest.json             # Extension manifest
│   ├── popup.html/js             # Extension UI
│   ├── content.js                # Content script
│   └── background.js             # Background service worker
├── .env                          # Environment variables
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── paperbiceps_logo.jpg          # Project logo
└── README.md                     # This file
```

## 🧪 How to Run Locally

1. **Clone the repo**
    ```bash
    git clone https://github.com/yourusername/PaperBiceps.git
    cd PaperBiceps
    ```

2. **Create a virtual environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r app/requirements.txt
    ```

4. **Add your API keys**  
   Create a `.env` file in the root directory and add:
    ```ini
    GEMINI_API_KEY=your_gemini_key_here
    DEEPGRAM_API_KEY=your_deepgram_key_here
    ```

5. **Run the backend API**
    ```bash
    cd app
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    The API will be available at `http://localhost:8000`
    - API documentation: `http://localhost:8000/docs`
    - Health check: `http://localhost:8000/health`

6. **Load Chrome Extension**
    - Open `chrome://extensions/`
    - Enable "Developer mode"
    - Click "Load unpacked" and select the `extension/` folder
    - The extension microphone will appear on webpages

---

## 🛠️ Known Limitations

- 🐢 Script + Audio generation can be a little slow, especially for long files or limited bandwidth.
- 🤖 Gemini API occasionally throws rate/resource errors if overused or overloaded if using under free tier

---

## 🤝 Contributing

This is an open source project, and contributions are warmly welcome!  
If you're interested in:

- 🏗️ **Improving the modular architecture** - Adding new services, optimizing existing ones
- ⚡ **Performance optimization** - Speeding up script generation and audio synthesis
- 🎭 **Voice enhancement** - Adding emotion and style using TTS attributes
- 🌍 **Multi-language support** - Extending to non-English content


Feel free to open a pull request or issue 🙌

Start by forking the repo, creating a new branch, and submitting a PR.

---

## 🧠 Ideal Use Cases

- Listen to any important documnet on the go.
- Turn research papers into explainable podcast summaries
- Convert blog posts or newsletters into audio for listeners
- Build your own AI-powered podcast channel
- Help visually impaired users "listen" to any document

---

## 📜 License

Licensed under the MIT License.
