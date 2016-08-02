package net.momoka.jetty;

import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.ServerConnector;
import org.eclipse.jetty.server.handler.HandlerCollection;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.eclipse.jetty.util.thread.QueuedThreadPool;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main (String[] args) throws Exception {

    String jettyHost = System.getProperty("jetty.host", "0.0.0.0");
    int jettyPort = Integer.parseInt(
      System.getProperty("jetty.port", "3000"));

    QueuedThreadPool pool = new QueuedThreadPool();
    pool.setMinThreads(10);
    pool.setMaxThreads(50);

    Server server = new Server(pool);
    ServerConnector connector = new ServerConnector(server);
    connector.setHost(jettyHost);
    connector.setPort(jettyPort);
    connector.setIdleTimeout(30000);

    ServletContextHandler context = new ServletContextHandler(
      ServletContextHandler.SESSIONS);
    context.setContextPath("/");

    HandlerCollection handlers = new HandlerCollection();
    handlers.addHandler(context);

    ServletHolder servletHodler = context.addServlet(BaseServlet.class, "/");

    server.addConnector(connector);
    // server.setHandler(handlers);
    server.manage(pool);
    server.start();
  }

}
