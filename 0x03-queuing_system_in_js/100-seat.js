import { promisify } from 'util';
import { createClient } from 'redis';
import { createQueue } from 'kue';
import express from 'express';

let reservationEnabled = true;
const client = createClient();

client.on('error', (err) => {
  console.log(`Error: ${err}`);
});

function reserveSeat(number) {
  return client.set('available_seats', number);
}

function getAvailableSeats() {
  return promisify(client.get).bind(client)('available_seats');
}

const queue = createQueue();
const app = express();

app.get('/available_seats', (req, res) => {
  getAvailableSeats().then((seats) => {
    res.json({ numberOfAvailableSeats: seats });
  });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }
  const job = queue.create('reserve_seat');

  job
    .on('complete', (status) => {
      console.log(`Seat reservation job ${job.id} completed`);
    })
    .on('failed', (err) => {
      console.log(`Seat reservation job ${job.id} failed: ${err}`);
    })
    .save((err) => {
      if (err) return res.json({ status: 'Reservation failed' });
      return res.json({ status: 'Reservation in process' });
    });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    let available = await getAvailableSeats();
    available -= 1;
    reserveSeat(available);
    if (available >= 0) {
      if (available === 0) reservationEnabled = false;
      done();
    }
    done(new Error('Not enough seats available'));
  });
});

app.listen(1245, () => {
  reserveSeat(50);
  reservationEnabled = true;
  console.log('Server is running on port 1245');
});
