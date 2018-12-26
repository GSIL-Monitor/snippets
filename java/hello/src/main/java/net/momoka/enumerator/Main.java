package net.momoka.enumerator;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  public enum Planet {

    EARTH(3),
    MARS(4);

    private int v;

    Planet(int v) {
      this.v = v;
    }

  }

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) {

    LOGGER.debug("{}", Planet.EARTH);
    LOGGER.debug("{}", Planet.EARTH.v);
    LOGGER.debug("{}", Planet.EARTH.ordinal());

    LOGGER.debug("{}", Planet.MARS);
    LOGGER.debug("{}", Planet.MARS.v);
    LOGGER.debug("{}", Planet.MARS.ordinal());
  }

}
