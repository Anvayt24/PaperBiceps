from pydoc import text
import google.generativeai as genai
import os
import spacy
from dotenv import load_dotenv
load_dotenv()

nlp = spacy.load("en_core_web_sm")
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def gemini_setup(GEMINI_API_KEY):
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel("gemini-2.5-pro")

#chunking using nltk
def chunk_text(text, max_words=2500 , max_chunks=3):
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

#building prompts
def build_prompt(chunk):
    return f"""
You're Sky, a warm and witty Indian podcast host. You're interviewing an expert about the following topic.

Begin the script with:
Sky: Hey everyone! Welcome back to The Paper Biceps Show , I am Sky your host .
Sky: So , Would you rather watch your parents have dinner in silence for the rest of your life, or join in and listen to this podcast? Haha, just kidding!

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

# podcast style dialogue
def generate_podcast_script(model, full_text):
    chunks = chunk_text(full_text, max_words=2500 , max_chunks=3)
    full_dialogue = ""

    for i , chunk in enumerate(chunks):
        prompt = build_prompt(chunk)
        try :
            response = model.generate_content(prompt)
            full_dialogue += f"\n\n🎧 segment{i+1}:\n" + response.text
        except Exception as e:
            print(f"Error generating text for chunk {i+1}: {e}")

    return full_dialogue.strip()
            