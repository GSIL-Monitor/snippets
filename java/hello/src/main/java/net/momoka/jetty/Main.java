package net.momoka.jetty;

import org.eclipse.jetty.server.NCSARequestLog;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.ServerConnector;
import org.eclipse.jetty.server.handler.HandlerCollection;
import org.eclipse.jetty.server.handler.RequestLogHandler;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.eclipse.jetty.util.thread.QueuedThreadPool;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class Resource {
  public Resource () {
  }

  public String getPath () {
    String rv =
      getClass().getClassLoader().getResource("").toExternalForm();
    return rv;
  }
}


public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);


  public static void main (String[] args) throws Exception {

    String jettyHost = System.getProperty("jetty.host", "0.0.0.0");
    int jettyPort = Integer.parseInt(
      System.getProperty("jetty.port", "3000"));
    String alogPath = System.getProperty("config.alogPath", "logs/");

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

    Resource r = new Resource();
    String resourceBase = r.getPath();
    LOGGER.debug(resourceBase);
    context.setResourceBase(resourceBase);

    String logFilePath = String.format(
      "%s/yyyy_mm_dd.request.log", alogPath);

    // RequestLogHandler
    NCSARequestLog requestLog = new NCSARequestLog();
    requestLog.setFilename(logFilePath);
    requestLog.setFilenameDateFormat("yyyy_MM_dd");
    requestLog.setRetainDays(30);
    requestLog.setAppend(true);
    requestLog.setExtended(true);
    requestLog.setLogCookies(false);
    requestLog.setLogTimeZone("Asia/Shanghai");

    RequestLogHandler requestLogHandler  = new RequestLogHandler();
    requestLogHandler.setRequestLog(requestLog);

    HandlerCollection handlers = new HandlerCollection();
    handlers.addHandler(context);
    handlers.addHandler(requestLogHandler);

    // ServletHolder
    context.addServlet(StaticServlet.class, "/static/*");
    context.addServlet(IndexServlet.class, "/");

    server.addConnector(connector);
    server.setHandler(handlers);
    server.manage(pool);


    TemplateLoader loader = TemplateLoader.getInstance();
    loader.init();

    server.start();
  }

}
