package net.momoka.nio.socket;

import java.io.IOException;
import java.net.SocketException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.DatagramChannel;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class UDP {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(UDP.class);

  protected int port;
  protected DatagramChannel channel;


  public UDP(int port) {
    this.port = port;
  }

  public void start()
    throws IOException, SocketException, InterruptedException {
    channel = DatagramChannel.open();
    channel.configureBlocking(false);
    channel.socket().bind(new InetSocketAddress(port));

    loop();
  }

  protected void loop() throws IOException, InterruptedException {
    ByteBuffer b = ByteBuffer.allocate(4);

    for(;;) {
      channel.receive(b);
      byte[] ba = b.array();
      if (ba.length <= 4) {
        b.clear();
        Thread.sleep(500);
      }
      LOGGER.debug("\"{}\"", new String(ba));
    }
  }

}
