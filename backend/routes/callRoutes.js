import express from 'express';
import { startCall } from '../controller/callController.js';

const router = express.Router();

router.post('/start-call', startCall);

export default router;