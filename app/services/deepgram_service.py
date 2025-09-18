import httpx
from typing import Optional
from pydub import AudioSegment
from fastapi import HTTPException
from config import settings
from app.utils.file_utils import generate_temp_filename, cleanup_file


class DeepgramService:
    TTS_URL = "https://api.deepgram.com/v1/speak"
    
    def _get_headers(self) -> dict[str, str]:
        if not settings.is_deepgram_configured:
            raise HTTPException(
                status_code=500, 
                detail="Deepgram API key not configured"
            )
        return {
            "Authorization": f"Token {settings.DEEPGRAM_API_KEY}",
            "Content-Type": "application/json"
        }
    
    async def generate_audio(self, text: str, model: str = "aura-2-thalia-en") -> str:
        if not text.strip():
            raise HTTPException(
                status_code=400, 
                detail="Text cannot be empty"
            )
        payload = {"text": text}
        try:
            async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
                response = await client.post(
                    f"{self.TTS_URL}?model={model}",
                    headers=self._get_headers(),
                    json=payload
                )
            if response.status_code == 200:
                audio_file = generate_temp_filename("deepgram_audio", "mp3")
                with open(audio_file, "wb") as f:
                    f.write(response.content)
                return audio_file
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Deepgram API error: {response.text[:200]}"
                )
        except httpx.TimeoutException as e:
            # Gateway Timeout when Deepgram does not respond in time
            raise HTTPException(
                status_code=504,
                detail=f"Timeout connecting to Deepgram (check internet connectivity or try again): {str(e)}"
            )
        except httpx.ConnectError as e:
            # DNS resolution or connection failure
            message = str(e)
            if "getaddrinfo failed" in message:
                detail = "DNS resolution failed for Deepgram API host. Check your internet connection and DNS settings."
            else:
                detail = "Unable to connect to Deepgram API. Check your internet connection or firewall."
            raise HTTPException(
                status_code=503,
                detail=f"{detail} Underlying error: {message}"
            )
        except httpx.RequestError as e:
            # Other client-side network issues
            raise HTTPException(
                status_code=503, 
                detail=f"Network error connecting to Deepgram: {str(e)}"
            )
    
    def _parse_dialogue_line(self, line: str) -> Optional[tuple[str, str]]:
        line = line.replace("\u200b", "").replace("\u00a0", "").strip()
        if not line or ":" not in line:
            return None
        parts = line.split(":", 1)
        if len(parts) != 2:
            return None
        speaker = parts[0].strip().lower()
        text = parts[1].strip()
        if speaker not in settings.SPEAKER_VOICES:
            return None
        if not text:
            return None
        return speaker, text
    
    async def generate_podcast_audio(self, script_path: str, output_path: str) -> None:
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise HTTPException(
                status_code=404, 
                detail=f"Script file not found: {script_path}"
            )
        audio_segments = []
        temp_files = []
        for line_num, line in enumerate(lines, 1):
            dialogue = self._parse_dialogue_line(line)
            if not dialogue:
                continue
            speaker, text = dialogue
            voice_model = settings.SPEAKER_VOICES[speaker]
            try:
                audio_file = await self.generate_audio(text, voice_model)
                temp_files.append(audio_file)
                segment = AudioSegment.from_mp3(audio_file)
                audio_segments.append(segment)
                if line_num < len(lines):
                    pause = AudioSegment.silent(duration=1000)
                    audio_segments.append(pause)
            except Exception as e:
                for temp_file in temp_files:
                    cleanup_file(temp_file)
                raise HTTPException(
                    status_code=500,
                    detail=f"Error generating audio for line {line_num}: {str(e)}"
                )
        if not audio_segments:
            raise HTTPException(
                status_code=400,
                detail="No valid dialogue found in script"
            )
        try:
            final_audio = sum(audio_segments)
            final_audio.export(output_path, format="mp3")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error combining audio segments: {str(e)}"
            )
        finally:
            for temp_file in temp_files:
                cleanup_file(temp_file)

    async def test_connectivity(self) -> dict:
        """Perform a lightweight connectivity check to Deepgram.
        Tries a very short TTS request and cleans up immediately.
        """
        if not settings.is_deepgram_configured:
            return {"configured": False, "reachable": False, "reason": "DEEPGRAM_API_KEY not configured"}
        try:
            # Use a very short text and default model
            audio_file = await self.generate_audio("test", "aura-2-thalia-en")
            # Clean up if a file was produced
            cleanup_file(audio_file)
            return {"configured": True, "reachable": True}
        except HTTPException as e:
            # Surface status and reason for diagnostics
            return {"configured": True, "reachable": False, "status": e.status_code, "reason": e.detail}
