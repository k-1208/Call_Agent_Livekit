import os
from typing import Dict, Any
from dotenv import load_dotenv
from livekit.plugins import deepgram, openai, elevenlabs, cartesia


load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

DEFAULT_STT_CONFIG = {
    "provider": "deepgram",
    "settings": {
        "filler_words": False,
        "model": "nova-2-general",
        "interim_results": False,
        "smart_format": True
    }
}

DEFAULT_LLM_CONFIG = {
    "provider": "openai",
    "settings": {
        "model": "gpt-4o-mini",
        "temperature": 0.0
    }
}

DEFAULT_TTS_CONFIG = {
    "provider": "cartesia",
    "settings": {
        "model": "sonic-english",
        "voice": "79a125e8-cd45-4c13-8a67-188112f4dd22"  # British Lady voice
    }
}

def get_stt_instance(stt_settings: dict[str, any] = None) -> any:
    stt_settings = stt_settings or DEFAULT_STT_CONFIG
    provider = stt_settings.get("provider", "deepgram")

    if provider == "deepgram":
        return deepgram.STT(
            filler_words=stt_settings.get("settings", {}).get("filler_words", False),
            model=stt_settings.get("settings", {}).get("model", "nova-2-general"),
            interim_results=stt_settings.get("settings", {}).get("interim_results", False),
            smart_format=stt_settings.get("settings", {}).get("smart_format", True),
        )
    
    raise ValueError(f"Unsupported STT provider: {provider}")
    
def get_llm_instance(llm_settings: Dict[str, Any] = None) -> Any:
    """Get LLM instance based on settings."""
    settings = llm_settings or DEFAULT_LLM_CONFIG
    
    return openai.LLM(
        model=settings.get("settings", {}).get("model", "gpt-4o-mini"),
        temperature=settings.get("settings", {}).get("temperature", 0.0)
    )

def get_tts_instance(tts_settings: dict[str, any] = None) -> any:
    tts_settings = tts_settings or DEFAULT_TTS_CONFIG
    provider = tts_settings.get("provider", "cartesia")
    
    if provider == "cartesia":
        return cartesia.TTS(
            model=tts_settings.get("settings", {}).get("model", "sonic-english"),
            voice=tts_settings.get("settings", {}).get("voice", "79a125e8-cd45-4c13-8a67-188112f4dd22")
        )
    elif provider == "openai":
        return openai.TTS(
            model=tts_settings.get("settings", {}).get("model", "tts-1"),
            voice=tts_settings.get("settings", {}).get("voice", "shimmer"),
            speed=tts_settings.get("settings", {}).get("speed", 1.15),
        )
    
    raise ValueError(f"Unsupported TTS provider: {provider}")


DEFAULT_AGENT_CONFIG = {
    "allow_interruptions": True,
    "preemptive_synthesis": False,
    "min_endpointing_delay": 2.5
}