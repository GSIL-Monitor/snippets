package pl.hachune;

import javax.servlet.ServletContext;
import javax.servlet.ServletRegistration;

import org.springframework.web.context.ContextLoaderListener;
import org.springframework.web.WebApplicationInitializer;
import org.springframework.web.context.support.XmlWebApplicationContext;
import org.springframework.web.servlet.DispatcherServlet;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class MyWebApplicationInitializer
  implements WebApplicationInitializer {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(MyWebApplicationInitializer.class);

  @Override
  public void onStartup(ServletContext container) {

    LOGGER.debug("=====> onStartup");

    XmlWebApplicationContext appContext = new XmlWebApplicationContext();
    appContext.setConfigLocation("classpath*:/dispatcher-servlet.xml");

    container.addListener(new ContextLoaderListener(appContext));

    ServletRegistration.Dynamic dispatcher =
      container.addServlet(
        "dispatcher", new DispatcherServlet(appContext));

    dispatcher.setLoadOnStartup(1);
    dispatcher.addMapping("/");

    LOGGER.debug("onStartup <=====");

  }

}
