package net.momoka.logback;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.LoggerContext;
import ch.qos.logback.classic.spi.ILoggingEvent;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger("chen_lei");

  public Main() {

  }

  public static void main(String[] args) {
    LoggerContext ctx = (LoggerContext) LoggerFactory.getILoggerFactory();
    AlertAppender app = new AlertAppender();
    app.setContext(ctx);
    app.start();

    ch.qos.logback.classic.Logger logger =
      (ch.qos.logback.classic.Logger) LoggerFactory.getLogger("chen_lei");
    logger.addAppender(app);
    logger.setLevel(Level.DEBUG);
    logger.setAdditive(true);

    LOGGER.debug("hello world");
  }
}
