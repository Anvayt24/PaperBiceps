"""
Gemini AI service for text generation and podcast scripts
"""
import google.generativeai as genai
import spacy
import traceback
from fastapi import HTTPException
from config import settings
from app.utils.file_utils import safe_get_gemini_text

# Load spaCy model for text chunking
nlp = spacy.load("en_core_web_sm")

def gemini_setup(api_key: str = None):
    """
    Setup and configure Gemini AI model
    
    Args:
        api_key: Gemini API key (uses settings if not provided)
        
    Returns:
        Configured Gemini model
    """
    api_key = api_key or settings.GEMINI_API_KEY
    if not api_key:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

def chunk_text(text: str, max_words: int = None, max_chunks: int = None) -> list:
    """
    Chunk text using spaCy for better sentence boundary detection
    
    Args:
        text: Text to chunk
        max_words: Maximum words per chunk
        max_chunks: Maximum number of chunks
        
    Returns:
        List of text chunks
    """
    max_words = max_words or settings.MAX_CHUNK_WORDS
    max_chunks = max_chunks or settings.MAX_CHUNKS
    
    doc = nlp(text)
    chunks = []
    current_chunk = ""
    current_length = 0

    for sent in doc.sents:
        words_in_sent = len(sent.text.split())
        if current_length + words_in_sent <= max_words:
            current_chunk += sent.text + " "
            current_length += words_in_sent
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sent.text + " "
            current_length = words_in_sent

    if current_chunk and len(chunks) < max_chunks:
        chunks.append(current_chunk.strip())

    return chunks

def build_podcast_prompt(chunk: str) -> str:
    """
    Build prompt for podcast script generation
    
    Args:
        chunk: Text chunk to base the podcast on
        
    Returns:
        Formatted prompt for Gemini
    """
    return f"""
You're Sky, a warm and witty Indian podcast host. You're interviewing an expert about the following topic.

Begin the script with:
Sky: Hey everyone! Welcome back to The Paper Biceps Show , I am Sky your host .

Goals:
- Ask curious, human-like questions like in a real podcast , natural and unscripted (not robotic).
- Base your questions on the content + follow up naturally.
- Use a friendly, light tone in conversation.
- Use ranveer allahbadia's tone and style for podcast script.
- add some humor and add reaction for it like haha etc
- add reactions like hmm... , oh wow ! 
- Format each line clearly using just `Sky:` and `Expert:` as speaker names.
- Do NOT use emojis, asterisks, markdown formatting, or section headers.
- Mention The Paper Biceps Show when you open or close.
- Limit the number of Q&A pairs suitable for a 5–7 minutes of podcast .

Format:

Sky: [question]  
Expert: [answer]

Here's the content to base it on:
\"\"\"
{chunk}
\"\"\"
"""

def generate_podcast_script(model, full_text: str) -> str:
    """
    Generate podcast script from text using Gemini AI
    
    Args:
        model: Configured Gemini model
        full_text: Full text to convert to podcast
        
    Returns:
        Generated podcast script
    """
    chunks = chunk_text(full_text)
    full_dialogue = ""

    for i, chunk in enumerate(chunks):
        prompt = build_podcast_prompt(chunk)
        try:
            response = model.generate_content(prompt)
            full_dialogue += f"\n\n🎧 segment{i+1}:\n" + response.text
        except Exception as e:
            print(f"Error generating text for chunk {i+1}: {e}")

    return full_dialogue.strip()

async def call_gemini_model(model, prompt: str) -> str:
    """
    Call Gemini model with error handling and multiple method attempts
    
    Args:
        model: Configured Gemini model
        prompt: Text prompt to send
        
    Returns:
        Generated text response
    """
    try:
        # Try common method names in order
        if hasattr(model, "generate"):
            resp = model.generate(prompt)
        elif hasattr(model, "create"):
            resp = model.create(prompt)
        elif hasattr(model, "chat"):
            resp = model.chat(prompt)
        elif hasattr(model, "generate_content"):
            resp = model.generate_content(prompt)
        else:
            # If model is a callable (some wrappers return a function)
            if callable(model):
                resp = model(prompt)
            else:
                raise AttributeError("Gemini model object has no known generate method.")
        
        return safe_get_gemini_text(resp)
    except Exception as e:
        print(f"[Gemini call error] {e}")
        traceback.print_exc()
        raise

async def generate_explanation_text(content: str, context: str = "") -> str:
    """
    Generate explanation text using Gemini AI
    
    Args:
        content: Content to explain
        context: Additional context for the explanation
        
    Returns:
        Generated explanation text
    """
    if not settings.is_gemini_configured:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")

    model = gemini_setup()
    prompt = f"""
You are an expert research assistant. Please provide a clear, concise explanation of the following content.

Context: {context}
Content: {content}

Please provide a brief explanation suitable for audio narration.
Keep it conversational and easy to understand.
"""
    explanation = await call_gemini_model(model, prompt)
    return explanation
