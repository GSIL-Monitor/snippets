package net.momoka.string;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  private static final String UUID = "B469E313678947C68AB47317A7BE25CE";

  public static void main(String[] args) {


    StringBuilder sb = new StringBuilder();

    sb.append(UUID.substring(0, 8));
    sb.append("-");
    sb.append(UUID.substring(8, 12));
    sb.append("-");
    sb.append(UUID.substring(12, 16));
    sb.append("-");
    sb.append(UUID.substring(16, 20));
    sb.append("-");
    sb.append(UUID.substring(20));

    LOGGER.debug("{}", sb.toString());

    String filePath = "/tmp/hello/world.txt";

    int n = filePath.lastIndexOf("/");
    LOGGER.debug(filePath.substring(0, n));
    LOGGER.debug(filePath.substring(n + 1, filePath.length()));

    LOGGER.debug("ffwjifw//".replaceAll("\\/+$", ""));

    String routingKey = "keys.update_state.hhh";

    String prefix = routingKey.substring(0, routingKey.indexOf("."));
    LOGGER.debug("prefix: {}", prefix);

  }
}
