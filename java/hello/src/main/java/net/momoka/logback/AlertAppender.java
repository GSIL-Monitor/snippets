package net.momoka.logback;

import ch.qos.logback.core.UnsynchronizedAppenderBase;
import ch.qos.logback.classic.spi.ILoggingEvent;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AlertAppender
  extends UnsynchronizedAppenderBase<ILoggingEvent> {

  public AlertAppender() {

  }

  @Override
  protected void append(ILoggingEvent event) {
    System.out.println("appended: " + event.getMessage());
  }

}
