package net.momoka.logback;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetSocketAddress;
import java.net.SocketException;
import java.util.Arrays;

import ch.qos.logback.classic.PatternLayout;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.AppenderBase;
import ch.qos.logback.core.status.ErrorStatus;

public class UdpAppender extends AppenderBase<ILoggingEvent> {

  private String host;
  private int port;

  private String pattern;
  private PatternLayout patternLayout;

  private DatagramSocket socket;

  public String getHost() {
    return host;
  }

  public void setHost(String host) {
    this.host = host;
  }

  public int getPort() {
    return port;
  }

  public void setPort(int port) {
    this.port = port;
  }

  public String getPattern() {
    return pattern;
  }

  public void setPattern(String pattern) {
    this.pattern = pattern;
  }

  public void start() {

    int errors = 0;

    try {
      socket = new DatagramSocket();
      socket.connect(new InetSocketAddress(host, port));
    } catch (SocketException e) {
      addStatus(new ErrorStatus("cannot create socket", this, e));
      errors++;
    }

    patternLayout = new PatternLayout();
    patternLayout.setContext(context);
    patternLayout.setPattern(pattern);
    // patternLayout.setOutputPatternAsHeader(outputPatternAsHeader);
    patternLayout.start();

    if (errors == 0) {
      super.start();
    }
    else {
    }
  }

  public void stop() {

    if (socket != null)
      socket.close();

    patternLayout.stop();
  }

  @Override
  protected void append(ILoggingEvent eventObject) {

    String log = patternLayout.doLayout(eventObject);

    byte[] bytes = log.getBytes();

    if (bytes.length < 65400) {
      DatagramPacket packet = new DatagramPacket(bytes, bytes.length);
      sendSinglePacket(packet);
    }
    else {
      int idx = 0;
      int left = bytes.length;
      while (left > 0) {
        byte[] b = Arrays.copyOfRange(bytes, idx, idx + 65400);
        DatagramPacket packet = new DatagramPacket(b, bytes.length);
        sendSinglePacket(packet);
        idx += 65400;
        left -= idx;
      }
    }
  }

  private void sendSinglePacket(DatagramPacket packet) {
    try {
      socket.send(packet);
    } catch (IOException e) {
      addStatus(new ErrorStatus("send error", this, e));
    }
  }
}
