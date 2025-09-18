import os
import traceback
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Query
from fastapi.responses import FileResponse
from app.services.scraping_service import extract_text
from app.services.gemini_service import gemini_setup, generate_podcast_script
from app.services.deepgram_service import DeepgramService
from app.utils.text_cleaning import clean_text
from app.utils.file_utils import cleanup_file, generate_temp_filename
from config import settings

router = APIRouter(prefix="/api", tags=["podcast"])

@router.post("/generate-podcast/")
async def generate_podcast(file: UploadFile = File(None), url: str = Form(None)):
    """generate podcast from uploaded file or current url"""
    if not file and not url:
        raise HTTPException(status_code=400, detail="Please provide either a file or a URL")

    try:
        if file:
            file_extension = os.path.splitext(file.filename)[1].lower()
            temp_file = generate_temp_filename("temp", file_extension.lstrip('.'))
            with open(temp_file, "wb") as f:
                f.write(await file.read())
            raw_text = extract_text(temp_file)
            cleanup_file(temp_file)
        else:
            raw_text = extract_text(url)

        cleaned_text = clean_text(raw_text)
        model = gemini_setup()
        podcast_script = generate_podcast_script(model, cleaned_text)

        script_path = generate_temp_filename("script", "txt")
        cleaned_script = podcast_script.replace("**Sky:**", "Sky:").replace("**Expert:**", "Expert:")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(cleaned_script)

        output_audio = generate_temp_filename("audio", "mp3")
        await DeepgramService().generate_podcast_audio(script_path, output_audio)

        cleanup_file(script_path)

        return FileResponse(
            output_audio,
            media_type="audio/mpeg",
            filename="podcast_audio.mp3",
            headers={"X-Temp-File": output_audio}
        )

    except HTTPException as he:
        # Preserve status code/details from underlying services (e.g., 503/504 from Deepgram)
        raise he
    except Exception as e:
        print("[Error in /generate-podcast/]", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating podcast: {str(e)}")

# for chrome extension
@router.get("/podcast")
async def generate_podcast_api(url: str = Query(...)):
    """geberate podcast. for chrome extension"""
    try:
        raw_text = extract_text(url)
        cleaned_text = clean_text(raw_text)

        model = gemini_setup()
        podcast_script = generate_podcast_script(model, cleaned_text)

        script_path = generate_temp_filename("script", "txt")
        cleaned_script = podcast_script.replace("**Sky:**", "Sky:").replace("**Expert:**", "Expert:")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(cleaned_script)

        output_audio = generate_temp_filename("audio", "mp3")
        await DeepgramService().generate_podcast_audio(script_path, output_audio)

        cleanup_file(script_path)

        return FileResponse(
            output_audio,
            media_type="audio/mpeg",
            filename="podcast_audio.mp3",
            headers={"X-Temp-File": output_audio}
        )
    except HTTPException as he:
        # Preserve status code/details from underlying services (e.g., 503/504 from Deepgram)
        raise he
    except Exception as e:
        print("[Error in /api/podcast]", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating podcast: {str(e)}")
