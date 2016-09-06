package net.momoka.cache;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  private static final String READ = "read";
  private static final String WRITE = "write";
  private static final String CACHE = "cache";
  private static final String FILENAME = "cache.dump";

  public Main() {

  }

  public static void main(String[] args) throws Exception {

    String action = System.getProperty("action", WRITE);

    Main main = new Main();

    if (READ.equals(action)) {
      main.read();
    }
    else if (WRITE.equals(action)) {
      main.write();
    }
    else if (CACHE.equals(action)) {
      main.cache();
    }

  }

  protected void read() throws IOException, ClassNotFoundException {
    FileInputStream fis = new FileInputStream(FILENAME);
    int ready = fis.available();
    byte[] b = new byte[ready];
    LOGGER.debug("read: {}", new String(b));
    fis.read(b);
    ByteArrayInputStream bais = new ByteArrayInputStream(b);
    ObjectInputStream ois = new ObjectInputStream(bais);
    Item item = (Item) ois.readObject();
    LOGGER.debug("item: {}", item.getName());
  }

  protected void write() throws IOException {
    Item item = new Item();
    item.setName("myName is nobody");
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    ObjectOutputStream oos = new ObjectOutputStream(baos);
    oos.writeObject(item);
    LOGGER.debug("wrote: {}", baos.toString());

    byte[] b = baos.toByteArray();

    FileOutputStream fos = new FileOutputStream(FILENAME);
    fos.write(b);
    fos.close();
  }

  protected void cache() {
    Item item = new Item();
    item.setName("myName is nobodyyyyyyyyy.");
    Item anotherItem;

    MemoryCache cache = new MemoryCache(10L);
    LOGGER.debug("cache: {}", cache.get("hello", Item.class));

    cache.put("hello", item, 500);
    LOGGER.debug("cache: storeSize: {}", cache.storeSize());

    anotherItem = cache.get("hello", Item.class);
    LOGGER.debug("cache: {}", anotherItem);
    if (anotherItem != null) {
      LOGGER.debug("cache: {}", anotherItem.getName());
    }

    try {
      Thread.sleep(550);
    }
    catch (InterruptedException e) {

    }
    LOGGER.debug("cache: storeSize: {}", cache.storeSize());

    anotherItem = cache.get("hello", Item.class);
    LOGGER.debug("cache: {}", anotherItem);

    long start = System.currentTimeMillis();
    for (int i = 0; i < 50000; i++) {
      cache.put("hello", item);
    }
    long end = System.currentTimeMillis();
    LOGGER.debug("put cost: {}ms", end - start);

    start = System.currentTimeMillis();
    for (int i = 0; i < 50000; i++) {
      cache.get("hello", Item.class);
    }
    end = System.currentTimeMillis();
    LOGGER.debug("get cost: {}ms", end - start);
  }
}
