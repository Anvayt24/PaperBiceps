# 🎙️ PaperBiceps — AI-Powered Podcaster

**Paper Biceps** is an AI tool that transforms any written content — research papers, articles, blogs, or documents — into realistic podcast conversations. It uses LLMs and TTS to simulate an actual podcast episode between a host and an expert.

---

## 🚀 Features

- 🧠 Gemini-powered summarization and script generation  
- 🎤 Dynamic host-expert style dialogue like a real podcast  
- 🗂️ Accepts PDF, TXT, DOCX, or URL input  
- 🎧 Dual-speaker audio generation using Edge TTS  
- 🎙️ Option to use Streamlit UI or FastAPI API  
- 🔊 Final podcast exported as an `.mp3`

---

## 🧰 Tech Stack

- Python 3.10+
- Streamlit
- FastAPI
- Edge TTS (Microsoft)
- Google Gemini API
- PyMuPDF, python-docx,trafilatura
- Pydub + FFmpeg

---

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
    pip install -r requirements.txt
    ```

4. **Add your API key**  
   Create a `.env` file and add:
    ```ini
    GEMINI_API_KEY=your_gemini_key_here
    ```

5. **Run the app**

    - For UI (Streamlit):
        ```bash
        streamlit run app.py
        ```

    - For backend API (FastAPI):
        ```bash
        uvicorn main:app --reload
        ```

---

## 🛠️ Known Limitations

- 🐢 Script + Audio generation can be slow, especially for long files or limited bandwidth.
- 🤖 Gemini API occasionally throws rate/resource errors if overused or overloaded if using under free tier

---

## 🤝 Contributing

This is an open source project, and contributions are warmly welcome!  
If you’re interested in:

- Improving performance or speed
- Adding voice emotion and style using edge tts attributes
- Supporting multi-language input
- Building a better UI or Chrome Extension
- Testing and debugging on different inputs

Feel free to open a pull request or issue 🙌

Start by forking the repo, creating a new branch, and submitting a PR.

---

## 🧠 Ideal Use Cases

- Turn research papers into explainable podcast summaries
- Convert blog posts or newsletters into audio for listeners
- Build your own AI-powered podcast channel
- Help visually impaired users "listen" to any document

---

## 📜 License

Licensed under the MIT License.
