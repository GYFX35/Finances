const request = require('supertest');
const db = require('../src/database');
const app = require('../src/index');

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
    expect(res.body.status).toEqual('completed');
    expect(res.body).toHaveProperty('transaction_id');
    expect(res.body.transaction_id).toMatch(/^lvuip_/);
  });

  it('should get a list of payouts', async () => {
    const res = await request(app).get('/payouts');
    expect(res.statusCode).toEqual(200);
    expect(res.body).toBeInstanceOf(Array);
  });
});
