package net.momoka.date;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Date;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main (String[] args) {

    Date date = new Date();

    String output = new SimpleDateFormat("yyyyMMdd").format(date);

    LOGGER.debug(output);

  }
}
