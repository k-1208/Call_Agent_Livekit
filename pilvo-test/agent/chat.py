import logging
import json
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from livekit import rtc
from livekit.agents import JobContext, AutoSubscribe, WorkerOptions, cli, JobExecutorType
from livekit.agents.voice import AgentSession, Agent
from config import get_stt_instance, get_llm_instance, get_tts_instance, DEFAULT_AGENT_CONFIG

# Simple system instructions for the agent
SYSTEM_INSTRUCTIONS = """You are a helpful voice assistant. Be concise and friendly in your responses. Always respond when someone talks to you."""

# Set up logging
logger = logging.getLogger(__name__)

async def create_chat_agent(ctx: JobContext, participant: rtc.Participant):
    """Create a simple voice assistant agent."""
    
    logger.info("Creating voice agent for participant: %s", participant.identity)
    
    # Test API keys
    import os
    logger.info("API Keys present - OpenAI: %s, Deepgram: %s, Cartesia: %s", 
                bool(os.getenv("OPENAI_API_KEY")), 
                bool(os.getenv("DEEPGRAM_API_KEY")), 
                bool(os.getenv("CARTESIA_API_KEY")))

    # Create an Agent first
    agent = Agent(
        instructions=SYSTEM_INSTRUCTIONS,
        llm=get_llm_instance(),
    )

    # Create agent session
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        stt=get_stt_instance(),
        llm=get_llm_instance(),
        tts=get_tts_instance(),
        allow_interruptions=DEFAULT_AGENT_CONFIG["allow_interruptions"],
    )

    logger.info("Starting agent session...")
    
    # Start the assistant session with agent and room
    await session.start(agent, room=ctx.room)
    logger.info("Agent session started, saying initial greeting...")
    
    try:
        # Say the initial greeting
        await session.say("Hello! How are you doing today?", allow_interruptions=True)
        logger.info("Greeting sent successfully")
    except Exception as e:
        logger.error("Error sending greeting: %s", e)
    
    logger.info("Agent is ready and listening...")
    
    # Return the session
    return session