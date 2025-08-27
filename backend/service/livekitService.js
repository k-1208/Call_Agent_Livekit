import { AgentDispatchClient } from 'livekit-server-sdk';
import { config } from '../config/envConfig.js';

// Create client once (Singleton pattern)
let dispatchClient;

function getDispatchClient() {
  if (!dispatchClient) {
    dispatchClient = new AgentDispatchClient(
      config.livekit.host,
      config.livekit.apiKey,
      config.livekit.apiSecret
    );
  }
  return dispatchClient;
}

export async function dispatchAgent(roomName, meta = {}) {
  const client = getDispatchClient();
  return client.createDispatch(
    roomName,
    config.livekit.agentName,
    JSON.stringify(meta)
  );
}