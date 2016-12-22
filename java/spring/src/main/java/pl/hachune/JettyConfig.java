package pl.hachune;

import java.util.Arrays;
import java.util.List;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.annotation.PropertySources;

@Configuration
@PropertySources(
  value={@PropertySource("classpath:config.properties"),
         @PropertySource(value="file:${config}",
                         ignoreResourceNotFound=true)}
)
public class JettyConfig {

  @Value("${jetty.hosts}")
  private String jettyHosts;

  @Value("${jetty.port}")
  private int jettyPort;

  @Value("${jetty.threads.min}")
  private int jettyTheadsMin;

  @Value("${jetty.threads.max}")
  private int jettyTheadsMax;

  @Bean
  public Jetty jetty() {
    Jetty rv = new Jetty();
    rv.setHosts(Arrays.asList(jettyHosts.split(",")));
    rv.setPort(jettyPort);

    rv.setMaxThreads(jettyTheadsMax);
    rv.setMinThreads(jettyTheadsMin);

    return rv;
  }
}
