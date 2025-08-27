import { SipClient } from 'livekit-server-sdk';
import { config } from '../config/envConfig.js';

let sipClient;

function getSipClient() {
  if (!sipClient) {
    sipClient = new SipClient(
      config.livekit.host,
      config.livekit.apiKey,
      config.livekit.apiSecret
    );
  }
  return sipClient;
}

export async function createSipTrunk({ name, address, number, trunkOptions }) {
  return getSipClient().createSipOutboundTrunk(
    name,
    address,
    [number],
    trunkOptions
  );
}

export async function createSipCall(trunkId, phoneNumber, roomName) {
  return getSipClient().createSipParticipant(trunkId, phoneNumber, roomName);
}