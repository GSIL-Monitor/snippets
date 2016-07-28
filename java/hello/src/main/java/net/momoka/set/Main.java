package net.momoka.set;

import java.util.Set;
import java.util.HashSet;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main (String[] args)  {
    Set<Long> s1 = new HashSet<Long>();
    Set<Long> s2 = new HashSet<Long>();

    s1.add(1L);
    s1.add(2L);
    s1.add(3L);
    s2.add(2L);
    s2.add(4L);

    LOGGER.debug("s1: {}", s1.toString());
    LOGGER.debug("s2: {}", s2.toString());

    Set<Long> inter = new HashSet<Long>(s2);
    inter.retainAll(s1);

    LOGGER.debug("intersection: {}", inter.toString());

    Set<Long> toAdd = new HashSet<Long>(s1);
    toAdd.removeAll(inter);

    LOGGER.debug("to add: {}", toAdd.toString());

    Set<Long> toRemove = new HashSet<Long>(s2);
    toRemove.removeAll(inter);

    LOGGER.debug("to remove: {}", toRemove.toString());

    for (Long e: toAdd) {
      s2.add(e);
    }

    for (Long e: toRemove) {
      s2.remove(e);
    }

    LOGGER.debug("result s2: {}", s2.toString());

  }

}
