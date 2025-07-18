const express = require('express');
const db = require('./database');
const app = express();
const port = 3000;

app.use(express.static('public'));
app.use(express.json());

app.post('/payouts', (req, res) => {
  const { amount, recipient } = req.body;
  const stmt = db.prepare('INSERT INTO transactions (amount, recipient, status) VALUES (?, ?, ?)');
  stmt.run(amount, recipient, 'pending', function (err) {
    if (err) {
      return res.status(500).send(err);
    }
    res.status(201).send({ id: this.lastID, status: 'pending' });
  });
  stmt.finalize();
});

app.get('/payouts', (req, res) => {
  db.all('SELECT * FROM transactions', (err, rows) => {
    if (err) {
      return res.status(500).send(err);
    }
    res.send(rows);
  });
});

app.get('/payouts/:id', (req, res) => {
  db.get('SELECT * FROM transactions WHERE id = ?', [req.params.id], (err, row) => {
    if (err) {
      return res.status(500).send(err);
    }
    if (!row) {
      return res.status(404).send('Transaction not found');
    }
    res.send(row);
  });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
