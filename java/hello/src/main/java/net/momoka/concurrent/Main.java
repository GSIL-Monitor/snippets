package net.momoka.concurrent;

import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import net.momoka.util.DigestUtil;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class DemoRunnable implements Runnable {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(DemoRunnable.class);

  private Random rnd = new Random();

  @Override
  public void run() {

    String payload = "hello";

    for (int i = 0; i < 10000000; i++) {
      DigestUtil.md5sum(payload);
    }

    LOGGER.debug("run done");
  }

}

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  protected ExecutorService pool;
  protected int poolSize = 1;

  public Main() {
    pool = Executors.newFixedThreadPool(poolSize);
  }

  public void run() {

    long s1 = System.currentTimeMillis();

    for (int i = 0; i < 100; i++) {
      long subs1 = System.currentTimeMillis();
      pool.execute(new DemoRunnable());
      long subCost = System.currentTimeMillis() - subs1;
      LOGGER.debug("subCost {}: {}", i, subCost);
    }

    long totalCost = System.currentTimeMillis() - s1;

    LOGGER.debug("totalCost: {}", totalCost);

    pool.shutdown();

  }

  public static void main(String[] args) {
    Main main = new Main();
    main.run();
  }
}
