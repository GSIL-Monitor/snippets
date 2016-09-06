package net.momoka.amqp;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Consumer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  protected static final String queueName = "just.a.test";

  public Main() {

  }

  public static void main(String[] args) throws IOException, TimeoutException {

    ConnectionFactory fac = new ConnectionFactory();
    fac.setUsername("guest");
    fac.setPassword("guest");
    fac.setVirtualHost("/");
    fac.setHost(System.getProperty("amqpHost"));
    fac.setPort(5672);
    fac.setAutomaticRecoveryEnabled(true);
    fac.setNetworkRecoveryInterval(3000);

    Connection connection = fac.newConnection();
    Channel channel = connection.createChannel();

    channel.queueDeclare(
      queueName,
      false, // durable
      false, // exclusive
      true,  // auto-delete
      null);
    channel.queueBind(
      queueName,
      System.getProperty("exchange"),
      System.getProperty("routingKey"));
    channel.close();

    for(int i = 0; i < 1024; i++) {
      Channel chan = connection.createChannel();
      Consumer c = new MyConsumer(chan);
      chan.basicConsume(queueName, false, c);
    }

    for(;;) {
      try {
        Thread.sleep(500);
      }
      catch(InterruptedException e) {
        break;
      }
    }

  }
}
