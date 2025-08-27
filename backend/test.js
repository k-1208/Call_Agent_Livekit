import express from 'express';
import dotenv from 'dotenv';
import {
  AgentDispatchClient,
  SipClient,
} from 'livekit-server-sdk';
import { configTrunk } from './config.js';

dotenv.config();
const app = express();
app.use(express.json());

const {
  LIVEKIT_HOST,
  LIVEKIT_API_KEY,
  LIVEKIT_API_SECRET,
  AGENT_NAME,    // match 'agent_name' in your worker
} = process.env;

if (!LIVEKIT_HOST || !LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
  throw new Error('Ensure LIVEKIT_HOST, LIVEKIT_API_KEY, LIVEKIT_API_SECRET are set');
}

const dispatchClient = new AgentDispatchClient(LIVEKIT_HOST, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);
const sipClient = new SipClient(LIVEKIT_HOST, LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

app.post('/start-call', async (req, res) => {
  const { phoneNumber, roomName } = req.body;

  if (!phoneNumber || !roomName) {
    return res.status(400).json({ error: 'phoneNumber and roomName required' });
  }

  try {
    // Get trunk configuration
    const config = await configTrunk();
    console.log('Trunk configuration:', config);
    const { name, address, number, trunkOptions } = config.trunk;
    const { auth_username: authUsername, auth_password: authPassword } = trunkOptions;
    
    // Create SIP outbound trunk
    const trunkInfo = await sipClient.createSipOutboundTrunk(
        name,
        address,
        [number],
        {
            auth_username: authUsername,
            auth_password: authPassword,
        }       
    );

    // Step 1: Dispatch agent to the room
    await dispatchClient.createDispatch(
      roomName,
      AGENT_NAME,
      JSON.stringify({ origin: 'sip_call' })
    );

    // Step 2: Place SIP call into room using the created trunk
    await sipClient.createSipParticipant(trunkInfo.sipTrunkId, phoneNumber, roomName);

    res.json({ 
      status: 'Agent dispatched and call initiated', 
      room: roomName,
      trunkId: trunkInfo.sipTrunkId 
    });
  } catch (error) {
    console.error('Error starting call:', error);
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => console.log('API server running on http://localhost:3000'));
    

