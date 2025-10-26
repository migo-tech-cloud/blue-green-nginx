const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

let chaosMode = false;

app.get('/version', (req, res) => {
  if (chaosMode) {
    return res.status(500).json({ error: 'Blue app in chaos mode' });
  }

  res.setHeader('X-App-Pool', 'blue');
  res.setHeader('X-Release-Id', process.env.RELEASE_ID_BLUE || 'blue-local');
  res.json({
    version: '1.0',
    pool: 'blue',
    releaseId: process.env.RELEASE_ID_BLUE || 'blue-local'
  });
});

app.get('/healthz', (req, res) => {
  if (chaosMode) return res.status(500).send('Unhealthy');
  res.send('OK');
});

app.post('/chaos/start', (req, res) => {
  chaosMode = true;
  res.send('Chaos started for blue');
});

app.post('/chaos/stop', (req, res) => {
  chaosMode = false;
  res.send('Chaos stopped for blue');
});

app.listen(port, () => {
  console.log(`Blue app running on port ${port}`);
});
