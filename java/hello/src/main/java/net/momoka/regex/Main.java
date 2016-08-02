package net.momoka.regex;

import java.util.regex.Pattern;
import java.util.regex.Matcher;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  private static final Pattern UUID = Pattern.compile(
    "^[0-9a-z]{8}\\-[0-9a-z]{4}\\-[0-9a-z]{4}\\-[0-9a-z]{4}\\-[0-9a-z]{12}$");

  public static void main (String[] args) {

    Matcher m = UUID.matcher(
      "D0909CBB-66A5-49F3-B537-CD9051237237".toLowerCase());

    if (m.matches()) {
      LOGGER.debug("matcher: {}", m.toString());
      LOGGER.debug("matched: {}", m.group(0));
    }
    else {
      LOGGER.debug("not match!");
    }
  }
}
