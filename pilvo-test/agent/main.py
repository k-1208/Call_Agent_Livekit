import logging
import json

from livekit import rtc
from livekit.agents import JobContext, AutoSubscribe, WorkerOptions, cli, JobExecutorType, JobProcess
from livekit.plugins import silero
from chat import create_chat_agent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def prewarm(proc: JobProcess):
    try:
        logger.info("Prewarming: Loading VAD model")
        proc.userdata["vad"] = silero.VAD.load(min_silence_duration=2.5, max_buffered_speech=180)
        logger.info("VAD model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading VAD in prewarm: {e}")
        raise

async def create_agent(ctx: JobContext, participant: rtc.Participant):
    """Create and start the chat agent for the participant."""
    try:
        metadata = json.loads(participant.metadata) if participant.metadata else {}
        logger.info("Creating agent with metadata: %s", metadata)
        
        # Ensure VAD is available, if not create it
        if "vad" not in ctx.proc.userdata:
            logger.warning("VAD not found in userdata, creating new instance")
            ctx.proc.userdata["vad"] = silero.VAD.load(min_silence_duration=2.5, max_buffered_speech=180)
        
        return await create_chat_agent(ctx, participant)
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        # Fallback: ensure VAD exists before retry
        if "vad" not in ctx.proc.userdata:
            logger.info("Creating VAD as fallback")
            ctx.proc.userdata["vad"] = silero.VAD.load(min_silence_duration=2.5, max_buffered_speech=180)
        return await create_chat_agent(ctx, participant)

async def entrypoint(ctx: JobContext):
    """Main entry point that determines which agent to use."""
    try:
        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
        # wait for participant to connect
        participant = await ctx.wait_for_participant()
        logger.info("Participant connected: %s", participant)

        # Create appropriate agent based on metadata
        await create_agent(ctx, participant)

    except Exception as e:
        logger.error("Error in entrypoint: %s", str(e))
        raise

# initialize worker with agents waiting for participants
if __name__ == "__main__":
    options = WorkerOptions(
        entrypoint_fnc=entrypoint,
        port=8080,
        job_executor_type=JobExecutorType.PROCESS,
        prewarm_fnc=prewarm,
        agent_name="outbound-caller",
    )
    cli.run_app(options)