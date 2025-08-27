import express from 'express';
import dotenv from 'dotenv';
import callRoutes from './routes/callRoutes.js';

dotenv.config();

const app = express();
app.use(express.json());

// API Routes
app.use('/api', callRoutes);

// Start Server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`API server running on http://localhost:${PORT}`);
});