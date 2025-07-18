const request = require('supertest');
const express = require('express');
const db = require('../src/database');

const app = express();
app.use(express.json());
require('../src/index'); // This will attach the routes to the app

describe('API Endpoints', () => {
  beforeAll((done) => {
    db.serialize(() => {
      db.run('DELETE FROM transactions');
      done();
    });
  });

  it('should create a new payout', async () => {
    const res = await request(app)
      .post('/payouts')
      .send({ amount: 100, recipient: 'test' });
    expect(res.statusCode).toEqual(201);
    expect(res.body).toHaveProperty('id');
  });

  it('should get a list of payouts', async () => {
    const res = await request(app).get('/payouts');
    expect(res.statusCode).toEqual(200);
    expect(res.body).toBeInstanceOf(Array);
  });
});
