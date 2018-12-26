package net.momoka.hashring;

import com.liveprofile.hashring.HashRing;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) throws Exception {

    HashRing ring = new HashRing(1, HashRing.HashFunction.MD5);

    ring.addNode("redis://10.47.77.3/2");
    ring.addNode("redis://10.45.23.62/2");
    ring.addNode("redis://10.45.22.22/2");
    ring.addNode("redis://10.45.52.32/2");

    String key = "u:current:lppa:53975033";

    String node = ring.findNode(key);

    LOGGER.debug("node: {}", node);
  }
}
