package net.momoka;

import java.net.URL;
import java.util.ArrayList;
import java.util.EventListener;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.MultipartConfigElement;
import javax.servlet.Servlet;

import org.springframework.web.servlet.DispatcherServlet;
import org.springframework.web.context.ContextLoaderListener;
import org.springframework.web.context.support.XmlWebApplicationContext;

import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.ServerConnector;
import org.eclipse.jetty.server.handler.ContextHandler;
import org.eclipse.jetty.server.handler.HandlerCollection;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.eclipse.jetty.util.thread.QueuedThreadPool;
import org.eclipse.jetty.webapp.WebAppContext;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Jetty {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Jetty.class);

  private boolean initialized;

  private List<String> hosts;
  private int port;
  private String contextPath;
  private String resourcePath;

  private int minThreads = 16;
  private int maxThreads = 64;
  private int idleTimeout = 30000;

  private Server server;
  private QueuedThreadPool pool;

  public Jetty () {
    contextPath = "/";
    resourcePath = "./";
    hosts = new ArrayList<String>();
    hosts.add("127.0.0.1");

    port = 8000;

    initialized = false;
  }

  public void setContextPath(String p) {
    this.contextPath = p;
  }

  public void setMinThreads(int m) {
    this.minThreads = m;
  }

  public void setMaxThread(int m) {
    this.maxThreads = m;
  }

  public void setIdleTimeout(int i) {
    this.idleTimeout = i;
  }

  public void setHosts(List<String> hosts) {
    this.hosts = hosts;
  }

  public void setPort(int port) {
    this.port = port;
  }

  public void setResourcePath(String p) {
    this.resourcePath = p;
  }

  public void init() {
    pool = new QueuedThreadPool();
    pool.setMinThreads(this.minThreads);
    pool.setMaxThreads(this.maxThreads);

    server = new Server(pool);

    for (String host: hosts) {
      ServerConnector connector = new ServerConnector(server);
      connector.setHost(host);
      connector.setPort(port);
      connector.setIdleTimeout(idleTimeout);
      server.addConnector(connector);
    }

    ServletContextHandler ctxHandler = new ServletContextHandler(
      ServletContextHandler.SESSIONS);

    WebAppContext webAppContext = new WebAppContext();
    webAppContext.setContextPath(contextPath);
    webAppContext.setResourceBase(resourcePath);

    XmlWebApplicationContext appContext = new XmlWebApplicationContext();
    appContext.setConfigLocation("classpath*:/dispatcher-servlet.xml");

    webAppContext.addEventListener(new ContextLoaderListener(appContext));

    Servlet s = new DispatcherServlet(appContext);


    ServletHolder holder = new ServletHolder(s);

    holder.getRegistration().setMultipartConfig(
      new MultipartConfigElement(
        System.getProperty("java.io.tmpdir"),
        20971520, 83886080, 10));

    holder.setInitOrder(0);

    webAppContext.addServlet(holder, "/");

    HandlerCollection handlers = new HandlerCollection();
    handlers.addHandler(webAppContext);

    server.setHandler(handlers);
    server.manage(pool);

    initialized = true;
  }

  public void start() {

    if (!initialized)
      init();

    try {
      server.start();
    }
    catch (Exception e) {
      e.printStackTrace();
    }
  }

  public void stop() {

  }
}
