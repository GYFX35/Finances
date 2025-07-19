const express = require('express');
const db = require('./database');
const app = express();
const port = 3000;

app.use(express.static('public'));
app.use(express.json());

/**
 * @route POST /payouts
 * @group Payouts - Operations about payouts
 * @param {object} req.body.required - The payout object
 * @returns {object} 201 - The created payout object
 * @returns {Error}  500 - An error occurred
 */
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

/**
 * @route GET /payouts
 * @group Payouts - Operations about payouts
 * @returns {Array.<object>} 200 - An array of payout objects
 * @returns {Error}  500 - An error occurred
 */
app.get('/payouts', (req, res) => {
  db.all('SELECT * FROM transactions', (err, rows) => {
    if (err) {
      return res.status(500).send(err);
    }
    res.send(rows);
  });
});

/**
 * @route GET /payouts/{id}
 * @group Payouts - Operations about payouts
 * @param {integer} id.path.required - The ID of the payout to retrieve
 * @returns {object} 200 - The payout object
 * @returns {Error}  404 - Payout not found
 * @returns {Error}  500 - An error occurred
 */
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
