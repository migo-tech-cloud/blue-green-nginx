const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

let chaosMode = false;

app.get('/version', (req, res) => {
  if (chaosMode) {
    return res.status(500).json({ error: 'Green app in chaos mode' });
  }

  res.setHeader('X-App-Pool', 'green');
  res.setHeader('X-Release-Id', process.env.RELEASE_ID_GREEN || 'green-local');
  res.json({
    version: '1.0',
    pool: 'green',
    releaseId: process.env.RELEASE_ID_GREEN || 'green-local'
  });
});

app.get('/healthz', (req, res) => {
  if (chaosMode) return res.status(500).send('Unhealthy');
  res.send('OK');
});

app.post('/chaos/start', (req, res) => {
  chaosMode = true;
  res.send('Chaos started for green');
});

app.post('/chaos/stop', (req, res) => {
  chaosMode = false;
  res.send('Chaos stopped for green');
});

app.listen(port, () => {
  console.log(`Green app running on port ${port}`);
});
