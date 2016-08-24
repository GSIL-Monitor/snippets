package net.momoka.concurrent;

import java.util.Random;
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.ThreadPoolExecutor;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class DemoRunnable implements Runnable {

  private Random rnd = new Random();

  @Override
  public void run() {
    String s = null;
    for (;;) {
      if(rnd.nextLong() % 10 == 0)
        s.equals("");

      try {
        Thread.sleep(1500);
      }
      catch(InterruptedException e) {
        return;
      }
    }
  }

}

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  protected ExecutorService pool;
  protected int poolSize = 4;

  public Main() {
    pool = Executors.newFixedThreadPool(poolSize);
  }

  public void run() {
    int current;

    for (;;) {
      current = ((ThreadPoolExecutor) pool).getActiveCount();
      LOGGER.debug("current: {}", current);
      if (current != poolSize) {
        pool.execute(new DemoRunnable());
      }
      else {
        try {
          Thread.sleep(500);
        }
        catch (InterruptedException e) {
          return;
        }
      }
    }

  }

  public static void main(String[] args) {
    Main main = new Main();
    main.run();
  }
}
