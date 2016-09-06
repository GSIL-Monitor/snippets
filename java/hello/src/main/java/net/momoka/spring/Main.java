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

    User u = new User();
    u.setId(1);
    u.setUsername(new String(new char[256]).replace("\0", "1"));

    um.insert(u);
  }
}
