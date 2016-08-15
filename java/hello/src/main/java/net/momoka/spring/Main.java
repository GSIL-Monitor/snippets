package net.momoka.spring;

import java.util.Enumeration;
import java.util.List;
import java.util.Properties;


import org.apache.ibatis.annotations.Result;
import org.apache.ibatis.annotations.Results;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.
  AnnotationConfigApplicationContext;
import org.springframework.web.context.support.
  AnnotationConfigWebApplicationContext;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import net.momoka.spring.model.User;
import net.momoka.spring.mapper.db1.UserMapper;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) {

    AnnotationConfigWebApplicationContext ctx =
      new AnnotationConfigWebApplicationContext();

    ctx.register(Config.class);
    ctx.refresh();

    UserMapper um =
      ctx.getBean("userMapper", UserMapper.class);

    LOGGER.debug("{}", um);

    User u = um.select(1L);
    LOGGER.debug("{}", u);

    u.setUsername("username1");
    um.update(u);

    LOGGER.debug("{}", u);

    u = um.select(1L);
    LOGGER.debug("{}", u);

    List<User> us = um.all();

    for (User _u: us) {
      LOGGER.debug("{}", _u);
    }

    // User nu = new User();
    // nu.setId(3);
    // nu.setUsername("username3");
    //
    // um.insert(nu);
  }
}
