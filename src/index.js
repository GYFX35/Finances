const express = require('express');
const db = require('./database');
const { processLvuipVenturesPayout } = require('./payment-gateways');
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
app.post('/payouts', async (req, res) => {
  const { amount, recipient } = req.body;

  // 1. Create a pending transaction in the database
  const stmt = db.prepare('INSERT INTO transactions (amount, recipient, status) VALUES (?, ?, ?)');
  stmt.run(amount, recipient, 'pending', async function (err) {
    if (err) {
      return res.status(500).send(err);
    }
    const dbId = this.lastID;

    // 2. Process the payout via Lvuip Ventures API
    try {
      const result = await processLvuipVenturesPayout({ amount, recipient });

      // 3. Update the transaction in the database
      const updateStmt = db.prepare('UPDATE transactions SET status = ?, transaction_id = ? WHERE id = ?');
      updateStmt.run(result.status === 'success' ? 'completed' : 'failed', result.transaction_id || null, dbId, (updateErr) => {
        if (updateErr) {
          console.error(`Failed to update transaction ${dbId}: ${updateErr.message}`);
        }
      });
      updateStmt.finalize();

      res.status(201).send({ id: dbId, status: result.status === 'success' ? 'completed' : 'failed', transaction_id: result.transaction_id });
    } catch (error) {
      console.error(`Error processing payout: ${error.message}`);
      res.status(500).send({ error: 'Payout processing failed' });
    }
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

if (require.main === module) {
  app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
  });
}

module.exports = app;
