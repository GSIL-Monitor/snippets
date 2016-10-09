package net.momoka.udp;

import java.io.IOException;
import java.net.DatagramSocket;
import java.net.DatagramPacket;
import java.net.InetSocketAddress;
import java.net.SocketException;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import com.qianka.util.concurrent.RunnableFactory;
import com.qianka.util.concurrent.ThreadPool;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class UDPServer {

  protected DatagramSocket socket;
  protected ServerRunnableFactory serverFactory;
  protected WorkerRunnableFactory workerFactory;
  protected ThreadPool server;
  protected ThreadPool worker;
  protected int socketPoolSize = 1;
  protected int workerPoolSize = 2;
  protected String[] bindAddresses = null;
  protected int port = 0;
  protected boolean inited = false;
  protected BlockingQueue<byte[]> q = null;

  protected int bufSize = 1024;

  public UDPServer(int port) {
    this.port = port;
    this.q = new LinkedBlockingQueue<byte[]>();
  }

  public void setBindAddresses(String[] bindAddresses) {
    this.bindAddresses = bindAddresses;
  }

  public void setPort(int port) {
    this.port = port;
  }

  public void setSocketPoolSize(int p) {
    this.socketPoolSize = p;
  }

  public void setWorkerPoolSize(int p) {
    this.workerPoolSize = p;
  }

  public void setBufSize(int s) {
    this.bufSize = s;
  }

  public void init() throws SocketException {

    if (inited)
      return;

    socket = new DatagramSocket(null);

    if (bindAddresses != null && bindAddresses.length > 0) {
      for(int i = 0; i < bindAddresses.length; i++) {
        socket.bind(new InetSocketAddress(bindAddresses[i], port));
      }
    }
    else {
      socket.bind(new InetSocketAddress(4000));
    }

    serverFactory = new ServerRunnableFactory(socket, q);
    workerFactory = new WorkerRunnableFactory(q);
    server = new ThreadPool(
      "udp-server",
      socketPoolSize,
      1000L,
      serverFactory);

    worker = new ThreadPool(
      "udp-worker",
      workerPoolSize,
      1000L,
      workerFactory);

    inited = true;
  }

  public void start() throws SocketException {
    init();
    worker.start();
    server.start();
  }

  public void stop() {
    server.shutdown();
    worker.shutdown();
    socket.close();
    inited = false;
  }

}

class ServerRunnable implements Runnable {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(WorkerRunnable.class);

  protected DatagramSocket socket;
  protected BlockingQueue<byte[]> q;

  public ServerRunnable (DatagramSocket socket, BlockingQueue<byte[]> q) {
    this.q = q;
    this.socket = socket;
  }

  @Override
  public void run() {

    byte[] buf = new byte[1024];
    DatagramPacket packet = new DatagramPacket(buf, buf.length);

    try {
      for(;;) {
        socket.receive(packet);
        LOGGER.debug("I've got work to do!");
        byte[] b = packet.getData();
        q.put(b);
      }
    }
    catch(IOException e) {
      e.printStackTrace();
      return;
    }
    catch(InterruptedException e) {
      return;
    }
  }

}

class ServerRunnableFactory implements RunnableFactory {

  protected DatagramSocket socket;
  protected BlockingQueue<byte[]> q;

  public ServerRunnableFactory(
    DatagramSocket socket, BlockingQueue<byte[]> q) {
    this.socket = socket;
    this.q = q;
  }

  @Override
  public Runnable newRunnable() {
    ServerRunnable rv = new ServerRunnable(socket, q);
    return rv;
  }

}

class WorkerRunnable implements Runnable {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(WorkerRunnable.class);

  protected BlockingQueue<byte[]> q;

  public WorkerRunnable (BlockingQueue<byte[]> q) {
    this.q = q;
  }

  @Override
  public void run() {

    while(true) {
      try {
        byte[] payload = q.take();
        LOGGER.debug(new String(payload));
      }
      catch(InterruptedException e) {
        return;
      }
    }

  }
}

class WorkerRunnableFactory implements RunnableFactory {

  protected BlockingQueue<byte[]> q;

  public WorkerRunnableFactory(BlockingQueue<byte[]> q) {
    this.q = q;
  }

  @Override
  public Runnable newRunnable() {
    WorkerRunnable rv = new WorkerRunnable(q);
    return rv;
  }

}

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public Main() {

  }

  public static void main(String[] args) throws Throwable {

    UDPServer server = new UDPServer(4000);
    server.setWorkerPoolSize(16);
    server.start();

    for(int i = 0; i < 5; i++) {
      Thread.sleep(1000);
    }

    server.stop();

  }
}
