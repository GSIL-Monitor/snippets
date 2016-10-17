package net.momoka.nio.socket;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public Main() {

  }

  public static void main(String[] args) throws Exception {

    UDP u = new UDP(4000);
    u.start();

  }
}
