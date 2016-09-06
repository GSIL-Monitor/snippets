package net.momoka.kafka;

import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import kafka.consumer.ConsumerConfig;
import kafka.consumer.ConsumerIterator;
import kafka.consumer.KafkaStream;
import kafka.javaapi.consumer.ConsumerConnector;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class Consumer implements Runnable {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Consumer.class);
  private final KafkaStream stream;
  private final BlockingQueue<byte[]> queue;

  public Consumer(KafkaStream stream, BlockingQueue<byte[]> queue) {
    this.stream = stream;
    this.queue = queue;
  }

  @Override
  public void run() {
    ConsumerIterator<byte[], byte[]> it = stream.iterator();
    while (it.hasNext()) {
      byte[] msg = it.next().message();
      // System.out.println(msg);
      // LOGGER.info(msg);
      try {
        queue.put(msg);
      }
      catch(InterruptedException e) {
        return;
      }
    }
  }
}

class FileAppender implements Runnable {

  private final BlockingQueue<byte[]> queue;
  private final FileWriter fw;

  public FileAppender(BlockingQueue<byte[]> queue) throws IOException {
    this.fw = new FileWriter("hera.sql.txt", true);
    this.queue = queue;
  }

  @Override
  public void run() {
    byte[] msg;
    for(;;) {
      try {
        msg = queue.take();
        if (msg == null)
          continue;
        fw.write(new String(msg));
        fw.write("\n");
      }
      catch (InterruptedException e) {
        return;
      }
      catch (IOException e) {
        e.printStackTrace();
        return;
      }
    }
  }
}

public class Main {

  private static final int THREADS = 4;
  private static final String TOPIC = "hera.sql";

  private final ExecutorService pool;
  private ConsumerConnector consumer;
  private BlockingQueue<byte[]> queue;

  public Main() {
    pool = Executors.newFixedThreadPool(THREADS);
  }

  public void init() {
    Properties prop = new Properties();
    prop.put("zookeeper.connect", "n1397.ops.gaoshou.me:2181");
    prop.put("group.id", "test.chenlei");
    prop.put("auto.offset.reset", "largest");
    ConsumerConfig config = new ConsumerConfig(prop);
    consumer = kafka.consumer.Consumer.createJavaConsumerConnector(config);

    queue = new LinkedBlockingQueue<byte[]>();
  }

  public void run() throws IOException {
    Map<String, Integer> topicCountMap = new HashMap<String, Integer>();
    topicCountMap.put(TOPIC, THREADS);
    Map<String, List<KafkaStream<byte[], byte[]>>> consumerMap =
      consumer.createMessageStreams(topicCountMap);
    List<KafkaStream<byte[], byte[]>> streams = consumerMap.get(TOPIC);

    for (final KafkaStream stream: streams) {
      pool.submit(new Consumer(stream, queue));
    }

    FileAppender f = new FileAppender(queue);
    Thread t = new Thread(f);
    t.setDaemon(false);
    t.start();

    for (;;) {
      try {
        Thread.sleep(1000);
      }
      catch (InterruptedException e) {
        consumer.shutdown();
        pool.shutdown();
        return;
      }
    }
  }

  public static void main(String[] args) throws Exception {
    Main main = new Main();
    main.init();
    main.run();
  }
}
