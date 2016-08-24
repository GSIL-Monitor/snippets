package net.momoka.date;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main (String[] args) {

    Calendar now = Calendar.getInstance();

    now.add(Calendar.HOUR, 3);

    String output = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").
      format(now.getTime());

    LOGGER.debug(output);

  }
}
