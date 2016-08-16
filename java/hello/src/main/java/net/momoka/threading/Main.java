package net.momoka.threading;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.Random;
import java.util.Map;
import java.util.HashMap;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;


class Manager {

  private static Manager instance;

  public static Manager getInstance() {
    if (instance == null) {
      instance = new Manager();
    }
    return instance;
  }

  public Manager () {

  }

}


class Worker {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Worker.class);

  private BlockingQueue<String> queue;
  private WorkerThread w;
  private Thread t;

  public Worker() {
    this.queue = new LinkedBlockingQueue<String>();
  }

  public void addWork (String payload) throws InterruptedException {

    Manager m = Manager.getInstance();
    LOGGER.info("{}", System. identityHashCode(m));

    this.queue.put(payload);
  }

  public void run () {
    this.w = new WorkerThread(this.queue);
    this.t = new Thread(this.w);
    this.t.setDaemon(false);
    this.t.start();
  }

  public void terminate () throws InterruptedException {
    this.w.terminate();
    this.t.interrupt();
    this.t.join();
    this.w = null;
    this.t = null;
  }

}

class WorkerThread implements Runnable {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(WorkerThread.class);

  private BlockingQueue<String> queue;
  private volatile boolean running = true;

  public WorkerThread(BlockingQueue<String> queue) {
    this.queue = queue;
  }

  public void terminate() {
    this.running = false;
  }

  @Override
  public void run () {
    String payload = null;
    while (this.running) {
      try {
        payload = this.queue.take();
      }
      catch (InterruptedException e) {
        LOGGER.debug("WorkerThread interrupted");
        return;
      }

      if (payload == null) continue;
      LOGGER.debug("got payload: {}", payload);
    }

  }
}

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) throws InterruptedException {

    Date now = null;
    int num = 0;
    int poolSize = 0;
    Random rnd = new Random();

    BlockingQueue<String> workQueue = new LinkedBlockingQueue<String>();

    // ThreadPoolExecutor workerPool = new ThreadPoolExecutor(
    //   10, 15, 30000, TimeUnit.MICROSECONDS,
    //   new LinkedBlockingQueue<Runnable>());

    // for (int i = 0; i < 5; i++) {
    //   workerPool.execute(new Worker(workQueue));
    // }

    ConcurrentHashMap pool =
      new ConcurrentHashMap(new HashMap<Long, Worker>());

    for (int i = 0; i < 15; i++) {
	    now = new Date();
	    num = (now.getSeconds() / 10) + 1;

      poolSize = pool.size();
      LOGGER.info("poolSize: {}, num: {}", poolSize, num);
      while (poolSize != num) {
        if (poolSize > num) {
          long key = 0;
          List<Long> keys = Collections.list(pool.keys());
          for (long _key: keys) {
            key = _key;
            break;
          }
          Worker w = (Worker) pool.get(key);
          w.terminate();
          pool.remove(key);
        }
        else {
          Worker w = new Worker();
          long key = rnd.nextLong();
          LOGGER.debug("new key: {}", key);
          w.run();
          pool.put(key, w);
        }
        poolSize = pool.size();
      }

      Date date = new Date();
      String payload = date.toString();

      for (Object o: pool.values()) {
        Worker w = (Worker) o;
        // LOGGER.info(w.toString());
        w.addWork(payload);
      }
      Thread.sleep(1000);
    }

    for (Object o: pool.values()) {
      Worker w = (Worker) o;
      w.terminate();
    }
    pool.clear();
  }
}
