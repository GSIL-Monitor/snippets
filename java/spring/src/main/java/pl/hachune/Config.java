package pl.hachune;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.PropertyNamingStrategy;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.annotation.PropertySources;
import org.springframework.core.io.support.ResourcePatternResolver;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.scheduling.annotation.EnableScheduling;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.aliyuncs.profile.DefaultProfile;
import com.aliyuncs.profile.IClientProfile;
import com.aliyuncs.IAcsClient;
import com.aliyuncs.DefaultAcsClient;

import com.qianka.util.http.HttpService;

import pl.hachune.models.Person;
import pl.hachune.zeromq.Sub;

@Configuration
@PropertySources(
  value = {
    @PropertySource("classpath:config.properties"),
    @PropertySource(value="file:${config}", ignoreResourceNotFound=true)
  }
)
@EnableScheduling
@ComponentScan(basePackages="pl.hachune.scheduling")
public class Config {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Config.class);

  private ResourcePatternResolver resolver =
    new PathMatchingResourcePatternResolver(getClass().getClassLoader());

  @Value("${aliyun.access.key}")
  public String aliyunKey;

  @Value("${aliyun.access.secret}")
  public String aliyunSecret;

  @Value("${yuntongxun.accountSid}")
  public String ytxAccountSid;

  @Value("${yuntongxun.accountToken}")
  public String ytxAccountToken;

  @Value("${yuntongxun.appId}")
  public String ytxAppId;

  @Value("${yuntongxun.apiBase}")
  public String ytxApiBase;

  @Value("${yuntongxun.displayNumber}")
  public String ytxDisplayNumber;

  @Bean("acsClient")
  public IAcsClient acsClient() {

    LOGGER.debug("aliyun.access.key: {}", aliyunKey);
    LOGGER.debug("aliyun.access.secret: {}", aliyunSecret);

    IClientProfile profile = DefaultProfile.getProfile(
        "cn-hangzhou", aliyunKey, aliyunSecret);
    IAcsClient rv = new DefaultAcsClient(profile);
    return rv;
  }

  @Bean
  public List<Person> persons() {
    List<Person> rv = new ArrayList<Person>();

    Person p;
    p = new Person();
    p.setName("p1");
    rv.add(p);
    p = new Person();
    p.setName("p2");
    rv.add(p);
    p = new Person();
    p.setName("p3");
    rv.add(p);

    return rv;
  }

  @Bean
  public HttpService httpService() {
    HttpService rv = new HttpService();
    return rv;
  }

  @Bean
  public ObjectMapper objectMapper() {
    ObjectMapper rv = new ObjectMapper();
    rv.configure(
      DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    rv.configure(
      SerializationFeature.WRITE_NULL_MAP_VALUES, false);
    rv.setSerializationInclusion(Include.NON_NULL);
    rv.setPropertyNamingStrategy(
      PropertyNamingStrategy.CAMEL_CASE_TO_LOWER_CASE_WITH_UNDERSCORES);

    rv.configure(
      SerializationFeature.INDENT_OUTPUT, true);
    return rv;
  }

  @Bean
  public YuntongxunNotify yuntongxunNotify() {
    YuntongxunNotify rv = new YuntongxunNotify();
    rv.setAccountSid(ytxAccountSid);
    rv.setAccountToken(ytxAccountToken);
    rv.setAppId(ytxAppId);
    rv.setApiBase(ytxApiBase);
    rv.setDisplayNumber(ytxDisplayNumber);
    return rv;
  }

  @Bean
  public Sub subscriber() {
    Sub rv = new Sub();
    return rv;
  }


}
