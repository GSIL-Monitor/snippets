package net.momoka.hostname;

import java.net.InetAddress;
import java.net.UnknownHostException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);


  public static void main(String[] args) throws UnknownHostException {

    String hostname = InetAddress.getLocalHost().getHostName();

    LOGGER.debug(hostname);

  }

}
