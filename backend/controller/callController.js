import { configTrunk } from '../config/configTrunk.js';
import { dispatchAgent } from '../service/livekitService.js';
import { createSipCall, createSipTrunk } from '../service/sipService.js';

export async function startCall(req, res) {
  const { phoneNumber, roomName } = req.body;

  if (!phoneNumber || !roomName) {
    return res.status(400).json({ error: 'phoneNumber and roomName required' });
  }

  try {
    const config = await configTrunk();
    const { name, address, number, trunkOptions } = config.trunk;

    const trunkInfo = await createSipTrunk({ name, address, number, trunkOptions });
    await dispatchAgent(roomName, { origin: 'sip_call' });
    await createSipCall(trunkInfo.sipTrunkId, phoneNumber, roomName);

    res.json({
      status: 'Agent dispatched and call initiated',
      room: roomName,
      trunkId: trunkInfo.sipTrunkId
    });
  } catch (error) {
    console.error('Error starting call:', error);
    res.status(500).json({ error: error.message });
  }
}
