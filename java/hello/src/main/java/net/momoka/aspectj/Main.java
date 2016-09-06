package net.momoka.aspectj;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) {
    // Aop aop = new Aop();
    Db db = new Db();

    Long start = System.currentTimeMillis();

    LOGGER.debug(db.getSomething());
    LOGGER.debug(db.getSomething());
    LOGGER.debug(db.getSomething());

    Long end = System.currentTimeMillis();

    LOGGER.debug("cost: {}ms", end - start);
  }

}
