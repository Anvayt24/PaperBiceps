import os
import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models.explain_request import ExplainRequest
from app.services.scraping_service import extract_text
from app.services.gemini_service import generate_explanation_text
from app.services.deepgram_service import DeepgramService
from app.utils.text_cleaning import clean_text, extract_specific_content

router = APIRouter(prefix="/api/explain", tags=["explain"])

@router.post("/figure")
async def explain_figure(request: ExplainRequest):
    """generate audio explanation for any figure"""
    try:
        raw_text = extract_text(request.url)
        cleaned_text = clean_text(raw_text)

        figure_content = extract_specific_content(cleaned_text, request.figure_id, "figure")
        print(f"[explain_figure] extracted length={len(figure_content or '')}")
        
        explanation_text = await generate_explanation_text(
            figure_content, 
            f"Figure {request.figure_id} from the document"
        )
        audio_filename = await DeepgramService().generate_audio(explanation_text)

        if not os.path.exists(audio_filename):
            raise HTTPException(status_code=500, detail="Audio file not created")

        return FileResponse(
            audio_filename,
            media_type="audio/mpeg",
            filename=f"figure_{request.figure_id}_explanation.mp3",
            headers={"X-Temp-File": audio_filename}
        )
    except HTTPException:
        raise
    except Exception as e:
        print("[Error in /api/explain/figure]", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating figure explanation: {str(e)}")

@router.post("/section")
async def explain_section(request: ExplainRequest):
    """generate audio explanation for a specific section"""
    try:
        raw_text = extract_text(request.url)
        cleaned_text = clean_text(raw_text)

        section_content = extract_specific_content(cleaned_text, request.section, "section")
        if not section_content or len(section_content.strip()) < 50:
            section_content = cleaned_text[:1000]

        print(f"[explain_section] extracted length={len(section_content or '')}")
        
        explanation_text = await generate_explanation_text(
            section_content, 
            f"Section '{request.section}' from the document"
        )
        audio_filename = await DeepgramService().generate_audio(explanation_text)

        if not os.path.exists(audio_filename):
            raise HTTPException(status_code=500, detail="Audio file not created")

        return FileResponse(
            audio_filename,
            media_type="audio/mpeg",
            filename=f"{request.section.replace(' ', '_')}_explanation.mp3",
            headers={"X-Temp-File": audio_filename}
        )
    except HTTPException:
        raise
    except Exception as e:
        print("[Error in /api/explain/section]", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating section explanation: {str(e)}")
