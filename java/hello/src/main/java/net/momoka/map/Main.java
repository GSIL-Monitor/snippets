package net.momoka.map;

import java.util.Map;
import java.util.TreeMap;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main (String[] args) {

    Map<String, String> def = new TreeMap<String, String>();
    def.put("prop1", "value11");
    def.put("prop2", "value12");
    def.put("prop3", "value13");

    Map<String, String> over = new TreeMap<String, String>();
    def.put("prop2", "value22");
    def.put("prop3", "value23");

    def.putAll(over);

    LOGGER.debug("{}", def);
  }

}
