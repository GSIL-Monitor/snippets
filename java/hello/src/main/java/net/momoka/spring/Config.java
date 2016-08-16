package net.momoka.spring;

import java.beans.PropertyVetoException;
import java.io.IOException;
import java.util.Properties;
import javax.annotation.Resource;


import com.mchange.v2.c3p0.ComboPooledDataSource;
import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.annotation.MapperScan;
import org.mybatis.spring.mapper.MapperScannerConfigurer;
// import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.beans.factory.config.PropertiesFactoryBean;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.env.Environment;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.annotation.PropertySources;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Configuration
@PropertySources(
  value={@PropertySource("classpath:spring.properties"),
         @PropertySource(value="file:${config}",
                         ignoreResourceNotFound=true)}
)
public class Config {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Config.class);

  @Resource
  Environment env;

  private ComboPooledDataSource getDataSource(String name)
    throws PropertyVetoException {
    String key;

    LOGGER.debug("{}", env);

    key = String.format("database.%s.driver", name);
    String driverClass = env.getRequiredProperty(key);

    key = String.format("database.%s.host", name);
    String host = env.getRequiredProperty(key);

    key = String.format("database.%s.port", name);
    Integer port = env.getRequiredProperty(key, Integer.class);

    key = String.format("database.%s.username", name);
    String username = env.getRequiredProperty(key);

    key = String.format("database.%s.password", name);
    String password = env.getRequiredProperty(key);

    key = String.format("database.%s.dbname", name);
    String dbName = env.getRequiredProperty(key);

    ComboPooledDataSource rv = new ComboPooledDataSource();

    rv.setDriverClass(driverClass);
    String url = String.format(
      "jdbc:mysql://%s:%d/%s?allowMultiQueries=true",
      host, port, dbName);

    rv.setJdbcUrl(url);
    rv.setUser(username);
    rv.setPassword(password);
    rv.setInitialPoolSize(1);
    rv.setMinPoolSize(0);
    rv.setMaxPoolSize(4);

    return rv;
  }

  @Bean(name = "datasource1")
  public ComboPooledDataSource dataSource1() throws PropertyVetoException {
    ComboPooledDataSource rv = getDataSource("db1");
    return rv;
  }

  @Bean(name = "datasource2")
  public ComboPooledDataSource dataSource2() throws PropertyVetoException {
    ComboPooledDataSource rv = getDataSource("db2");
    return rv;
  }

  @Bean(name = "sqlSession1")
  public SqlSessionFactory sqlSessionFactory1() throws Exception {
    SqlSessionFactoryBean rv = new SqlSessionFactoryBean();
    rv.setDataSource(dataSource1());
    return rv.getObject();
  }

  @Bean(name = "sqlSession2")
  public SqlSessionFactory sqlSessionFactory2() throws Exception {
    SqlSessionFactoryBean rv = new SqlSessionFactoryBean();
    rv.setDataSource(dataSource2());
    return rv.getObject();
  }

  @Bean
  public static MapperScannerConfigurer mapperScanner1() {
    MapperScannerConfigurer rv = new MapperScannerConfigurer();
    rv.setSqlSessionFactoryBeanName("sqlSession1");
    rv.setBasePackage("net.momoka.spring.mapper.db1");
    return rv;
  }

  // @Bean
  // public static MapperScannerConfigurer mapperScanner2() {
  //   MapperScannerConfigurer rv = new MapperScannerConfigurer();
  //   rv.setSqlSessionFactoryBeanName("sqlSession2");
  //   rv.setBasePackage("net.momoka.spring.mapper.db2");
  //   return rv;
  // }
}
