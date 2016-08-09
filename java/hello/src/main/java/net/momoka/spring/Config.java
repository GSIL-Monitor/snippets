package net.momoka.spring;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class Config {

  @Bean
  public Hello hello() {
    return new Hello();
  };

}
