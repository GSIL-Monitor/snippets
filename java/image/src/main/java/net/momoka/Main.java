package net.momoka;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public Main() {

  }

  public static void main(String[] args) throws Throwable {


    Jetty jetty = new Jetty();
    jetty.start();

    for(;;) {
      Thread.sleep(1000);
    }

  }
}
