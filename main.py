
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from podcast_script import generate_podcast_script, gemini_setup
from podcast_audio import generate_audio
from file_handling import extract_text
from text_preprocess import clean_text
from dotenv import load_dotenv
import os
import asyncio
import uuid

app = FastAPI()
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

@app.post("/generate-podcast/")
async def generate_podcast(file: UploadFile = File(None), url: str = Form(None)):
    if not file and not url:
        raise HTTPException(status_code=400, detail="Please provide either a file or a URL")

    try:
        
        if file:
            file_extension = os.path.splitext(file.filename)[1].lower()
            temp_file = f"temp_{uuid.uuid4().hex}{file_extension}"
            with open(temp_file, "wb") as f:   
                f.write(await file.read())
            raw_text = extract_text(temp_file)   #extracting text
            os.remove(temp_file)
        else:
            raw_text = extract_text(url)

        cleaned_text = clean_text(raw_text) #cleaned the text

        model = gemini_setup(GEMINI_API_KEY)
        podcast_script = generate_podcast_script(model, cleaned_text)


        script_path = f"temp_script_{uuid.uuid4().hex}.txt" #saving tp temporary files
        cleaned_script = podcast_script.replace("**Sky:**", "Sky:").replace("**Expert:**", "Expert:")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(cleaned_script)

        # generating audio
        output_audio = f"temp_audio_{uuid.uuid4().hex}.mp3"
        await generate_audio(script_path, output_audio) #running the audio generation

        # Clean up script file
        os.remove(script_path)

        
        return FileResponse(
            output_audio,
            media_type="audio/mpeg",
            filename="podcast_audio.mp3",
            headers={"X-Temp-File": output_audio}  # Store temp file path for cleanup
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating podcast: {str(e)}")
