package net.momoka.logback;

import ch.qos.logback.core.UnsynchronizedAppenderBase;
import ch.qos.logback.classic.spi.ILoggingEvent;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AlertAppender
  extends UnsynchronizedAppenderBase<ILoggingEvent> {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(AlertAppender.class);

  public AlertAppender() {

  }

  @Override
  protected void append(ILoggingEvent event) {
    System.out.println("appended: " + event.getMessage());
    // LOGGER.debug("{}", event.getMessage());
  }

}
