package net.momoka.concurrent;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadFactory;

public class ThreadPool {

  protected List<Thread> threads;
  protected int poolSize;
  protected long interval;
  protected ThreadFactory threadFactory = Executors.defaultThreadFactory();
  protected RunnableFactory runnableFactory;
  protected Thread reapThread;
  protected boolean running = false;

  protected class Reaper implements Runnable {

    @Override
    public void run() {
      while(true) {
        reap();
        spawnMissing();
        try {
          Thread.sleep(interval);
        }
        catch(InterruptedException e) {
          return;
        }
      }
    }

  }

  public int getPoolSize() {
    return poolSize;
  }

  public void setPoolSize(int poolSize) {
    this.poolSize = poolSize;
  }

  public long getInterval() {
    return interval;
  }

  public void setInterval(long interval) {
    this.interval = interval;
  }

  public ThreadPool(
    int poolSize, long interval, RunnableFactory runnableFactory) {
    this.poolSize = poolSize;
    this.runnableFactory = runnableFactory;

    threads = new ArrayList<Thread>();

  }

  public void start() {
    running = true;
    Runnable r = new Reaper();
    reapThread = new Thread(r);
    reapThread.setDaemon(false);
    reapThread.start();
  }

  public int activeCount() {
    int rv = 0;
    for(Thread t: threads) {
      if (t.isAlive()) {
        rv++;
      }
    }
    return rv;
  }

  public void shutdown() {
    running = false;

    while (activeCount() > 0) {
      for(Thread t: threads) {
        if (t.isAlive()) {
          t.interrupt();
          try {
            t.join();
          }
          catch(InterruptedException e) {
            continue;
          }
        }
      }
    }

    if (reapThread != null) {
      reapThread.interrupt();
    }
  }

  protected void spawn() {
    Runnable r = runnableFactory.newRunnable();
    Thread t = threadFactory.newThread(r);
    t.setDaemon(false);
    t.start();
    threads.add(t);
  }

  protected void reap() {
    if (!running) return;

    List<Thread> toRemove = new ArrayList<Thread>();
    for(Thread t: threads) {
      if(t.isAlive())
        continue;
      toRemove.add(t);
    }
    threads.removeAll(toRemove);

  }

  protected void spawnMissing() {
    if (!running) return;

    while (activeCount() < poolSize) {
      spawn();
    }
  }

}
