import { createQueue } from "kue";

const queue = createQueue();
const data = { phoneNumber: '4153518780', message: 'verification code' };

const job = queue.create('push_notification_code', data).save((err) => {
  if (!err) console.log(`Notification job created: ${job.id}`);
});

job.on('complete', () => console.log('Notification job completed'));

job.on('failed', () => console.log('Notification job failed'));
