const { isFraudulent } = require('../src/fraud-detection');

test('should return false for a non-fraudulent transaction', () => {
  const transaction = { amount: 100, recipient: 'test' };
  expect(isFraudulent(transaction)).toBe(false);
});
