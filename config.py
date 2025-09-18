import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY')
    DEEPGRAM_API_KEY: str = os.getenv('DEEPGRAM_API_KEY')
    
    # CORS settings
    ALLOWED_ORIGINS: list = ["*"]  # In production, specify exact origins
    
    # Deepgram voice models
    SPEAKER_VOICES = {
        "sky": "aura-2-thalia-en",      # Female voice for host
        "expert": "aura-2-orion-en"     # Male voice for expert
    }
    
    # Text processing settings
    MAX_CHUNK_WORDS: int = 2500
    MAX_CHUNKS: int = 3
    
    # API timeouts
    HTTP_TIMEOUT: int = 60
    EXTERNAL_REQUEST_TIMEOUT: int = 15
    
    @property
    def is_gemini_configured(self) -> bool:
        """Check if Gemini API key is configured"""
        return bool(self.GEMINI_API_KEY)
    
    @property
    def is_deepgram_configured(self) -> bool:
        """Check if Deepgram API key is configured"""
        return bool(self.DEEPGRAM_API_KEY)

# Global settings instance
settings = Settings()
