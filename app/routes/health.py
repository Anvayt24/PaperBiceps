import traceback
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services.gemini_service import generate_explanation_text
from app.services.deepgram_service import DeepgramService
from config import settings

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():

    return {
        "status": "healthy", 
        "gemini_configured": settings.is_gemini_configured,
        "deepgram_configured": settings.is_deepgram_configured
    }

@router.get("/api/test/gemini")
async def test_gemini():
    try:
        if not settings.is_gemini_configured:
            return {"error": "GEMINI_API_KEY not configured"}
        
        explanation = await generate_explanation_text("This is a test content", "Test context")
        return {
            "status": "success", 
            "explanation": explanation, 
            "gemini_configured": True
        }
    except Exception as e:
        print("[Error in /api/test/gemini]", str(e))
        traceback.print_exc()
        return {
            "error": str(e), 
            "gemini_configured": False
        }

@router.get("/api/test/deepgram")
async def test_deepgram():
    """Connectivity test for Deepgram. Performs a tiny TTS request and reports reachability."""
    try:
        svc = DeepgramService()
        result = await svc.test_connectivity()
        return {"status": "ok", **result}
    except Exception as e:
        print("[Error in /api/test/deepgram]", str(e))
        traceback.print_exc()
        return {"status": "error", "error": str(e)}

@router.get("/")
async def root():
    return RedirectResponse(url="/docs")
