package net.momoka.spring;

import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) {

    ApplicationContext ctx =
      new AnnotationConfigApplicationContext(Config.class);

    Hello hello = ctx.getBean(Hello.class);
    LOGGER.debug(hello.getMessage());

  }

}
