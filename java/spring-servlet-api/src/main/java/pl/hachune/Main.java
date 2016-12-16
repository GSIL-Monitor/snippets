package pl.hachune;

import javax.servlet.Servlet;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.web.servlet.DispatcherServlet;
import org.springframework.web.context.ContextLoaderListener;
import org.springframework.web.context.support.XmlWebApplicationContext;
import com.qianka.util.jetty.Jetty;


public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public Main() {

  }

  public static void main(String[] args) {
    XmlWebApplicationContext appContext = new XmlWebApplicationContext();
    appContext.setConfigLocation("classpath*:/dispatcher-servlet.xml");

    Servlet s = new DispatcherServlet(appContext);

    Jetty jetty = new Jetty();
    jetty.addEventListener(new ContextLoaderListener(appContext));
    jetty.addHandlerMapping("/", s);
    jetty.start();
  }
}
