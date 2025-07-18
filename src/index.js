const express = require('express');
const app = express();
const port = 3000;

app.use(express.static('public'));
app.use(express.json());

app.post('/payouts', (req, res) => {
  res.status(201).send({ id: 'payout_123', status: 'pending' });
});

app.get('/payouts/:id', (req, res) => {
  res.send({ id: req.params.id, status: 'completed' });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
