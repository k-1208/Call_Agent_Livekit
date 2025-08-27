import dotenv from 'dotenv';
dotenv.config();

export const config = {
  port: process.env.PORT || 3000,
  livekit: {
    host: process.env.LIVEKIT_HOST,
    apiKey: process.env.LIVEKIT_API_KEY,
    apiSecret: process.env.LIVEKIT_API_SECRET,
    agentName: process.env.AGENT_NAME,
  }
};

if (!config.livekit.host || !config.livekit.apiKey || !config.livekit.apiSecret) {
  throw new Error('LIVEKIT_HOST, LIVEKIT_API_KEY, LIVEKIT_API_SECRET must be set');
}
