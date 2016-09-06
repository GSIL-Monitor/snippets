package net.momoka.cache;

import java.util.concurrent.ConcurrentHashMap;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InvalidClassException;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;



public class MemoryCache {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(MemoryCache.class);

  protected CleanupRunnable cleanupRunnable;
  protected Thread cleanupThread;

  protected ConcurrentHashMap<String, CacheItem> store;

  protected long cleanupInterval;

  protected class CacheItem {

    private byte[] value;
    private long timestamp;
    private long expiry;

    public byte[] getValue() {
      return value;
    }

    public void setValue(byte[] value) {
      this.value = value;
    }

    public long getTimestamp() {
      return timestamp;
    }

    public void setTimestamp(long timestamp) {
      this.timestamp = timestamp;
    }

    public long getExpiry() {
      return expiry;
    }

    public void setExpiry(long expiry) {
      this.expiry = expiry;
    }

    public CacheItem() {

    }

    public boolean isExpired() {
      long now = System.currentTimeMillis();
      return now - timestamp > expiry;
    }
  }

  protected class CleanupRunnable implements Runnable {

    protected boolean running;

    public CleanupRunnable() {
      running = true;
    }

    @Override
    public void run() {
      while(running) {
        try {
          cleanup();
          Thread.sleep(cleanupInterval);
        }
        catch (InterruptedException e) {
          running = false;
          return;
        }
      }
    }

    protected void cleanup() {
      for (String k : store.keySet()) {
        CacheItem v = store.get(k);
        if (v != null) {
          if (v.isExpired()) {
            store.remove(k);
          }
        }
      }
    }

    public void terminate() {
      running = false;
    }
  }



  public MemoryCache(long cleanupInterval) {

    this.cleanupInterval = cleanupInterval;

    store = new ConcurrentHashMap<String, CacheItem>();
    cleanupRunnable = new CleanupRunnable();
    cleanupThread = new Thread(cleanupRunnable);
    cleanupThread.setDaemon(true);
    cleanupThread.start();
  }



  public void put(String k, Serializable o) {
    try {
      this._put(k, o, Long.MAX_VALUE);
    }
    catch (IOException e) {

    }
  }

  public void put(String k, Serializable o, long expiry) {
    try {
      this._put(k, o, expiry);
    }
    catch (IOException e) {

    }
  }

  public <T> T get(String k, Class<T> valueType) {
    try {
      return this._get(k, valueType);
    }
    catch (IOException e) {
      return null;
    }
    catch (ClassNotFoundException err) {
      return null;
    }
  }

  public void remove(String k) {
    store.remove(k);
  }

  public long storeSize() {
    return store.size();
  }

  protected void _put(String k, Serializable o, long expiry)
    throws IOException {
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    ObjectOutputStream oos = new ObjectOutputStream(baos);
    oos.writeObject(o);
    byte[] b = baos.toByteArray();

    CacheItem item = new CacheItem();
    item.setValue(b);
    item.setTimestamp(System.currentTimeMillis());
    item.setExpiry(expiry);
    store.put(k, item);
  }

  protected <T> T _get(String k, Class<T> valueType)
    throws IOException, ClassNotFoundException {
    CacheItem item = store.get(k);
    if (item == null) {
      return null;
    }

    if (item.isExpired()) {
      // TODO: delete?
      return null;
    }

    byte[] b = item.getValue();
    ByteArrayInputStream bais = new ByteArrayInputStream(b);
    ObjectInputStream ois = new ObjectInputStream(bais);

    try {
      Object o = ois.readObject();
      return (T) o;
    }
    catch (InvalidClassException e) {
      e.printStackTrace();
      return null;
    }
  }
}
