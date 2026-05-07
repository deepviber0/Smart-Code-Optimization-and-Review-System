const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;
const AI_ENGINE_URL = process.env.AI_ENGINE_URL || 'http://127.0.0.1:5001';

app.use(cors());
app.use(express.json());

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.post('/api/analyze', async (req, res) => {
  try {
    const { code, language } = req.body;
    
    if (!code) {
      return res.status(400).json({ error: 'Code is required' });
    }

    const response = await axios.post(`${AI_ENGINE_URL}/analyze`, {
      code,
      language: language || 'javascript'
    });

    res.json(response.data);
  } catch (error) {
    console.error('Error analyzing code:', error.message);
    res.status(500).json({ 
      error: 'Failed to analyze code',
      details: error.response?.data || error.message
    });
  }
});

app.listen(PORT, () => {
  console.log(`Backend server running on port ${PORT}`);
});
