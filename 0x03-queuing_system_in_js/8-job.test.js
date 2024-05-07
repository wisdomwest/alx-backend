import { createQueue } from "kue";
import chai from "chai";
import sinon from "sinon";
import createPushNotificationsJobs from "./8-job";

const expect = chai.expect;

const queue = createQueue();

const jobs = [
  { phoneNumber: "1234567890", message: "Hello" },
];

describe('createPushNotificationsJobs', () => {
  beforeEach(() => {
    sinon.spy(console, 'log');
  });

  before(() => {
    queue.testMode.enter();
  });

  afterEach(() => {
    sinon.restore();
    queue.testMode.clear();
  });

  after(() => {
    queue.testMode.exit()
  });

  it('validates the jobs array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
  });

  it('creates two jobs', () => {
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(1);
  });

  it('logs the correct messages', () => {
    createPushNotificationsJobs(jobs, queue);
    queue.testMode.jobs[0].emit('complete');
    queue.testMode.jobs[0].emit('failed');
    queue.testMode.jobs[0].emit('progress');
    expect(console.log.calledWith('Notification job 1 completed')).to.be.true;
    expect(console.log.calledWith('Notification job 1 failed: undefined')).to.be.true;
    expect(console.log.calledWith('Notification job 1 100% complete')).to.be.true;
  });
});
