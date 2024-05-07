function createPushNotificationsJobs(jobs, queue) {
  if (!(jobs instanceof Array)) throw new Error('Jobs is not an array');

  for (let job of jobs) {
    job = queue.create('push_notification_code_3', job)
    job
      .on('complete', () => console.log(`Notification job ${job.id} completed`))
      .on('failed', (err) => console.log(`Notification job ${job.id} failed: ${err}`))
      .on('progress', (progress) => console.log(`Notification job ${job.id} ${progress}% complete`))
      .save((err) => {
        if (!err) console.log(`Notification job created: ${job.id}`);
      });
  }
}

module.exports = createPushNotificationsJobs;
