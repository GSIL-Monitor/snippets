package net.momoka;

import java.util.List;

import com.aliyun.oss.OSSClient;
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
import org.springframework.context.annotation.FilterType;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.annotation.PropertySources;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.converter.json
  .MappingJackson2HttpMessageConverter;
import org.springframework.stereotype.Controller;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.
  ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.
  WebMvcConfigurerAdapter;

import net.momoka.UploadService;
import net.momoka.UploadServiceImpl;

@EnableWebMvc
@Configuration
@PropertySources(
  value={@PropertySource("classpath:config.properties"),
         @PropertySource(value="file:${config}",
                         ignoreResourceNotFound=true)}
)
@ComponentScan(
  basePackages="net.momoka.controller",
  useDefaultFilters=false,
  includeFilters=@ComponentScan.Filter(
    value=Controller.class,
    type=FilterType.ANNOTATION)
)
public class WebConfig extends WebMvcConfigurerAdapter {

  @Value("${aliyun.oss.endpoint}")
  private String aliyunOssEndpoint;

  @Value("${aliyun.oss.access.id}")
  private String aliyunOssAccessId;

  @Value("${aliyun.oss.access.secret}")
  private String aliyunOssAccessSecret;

  @Value("${aliyun.oss.bucket}")
  private String aliyunOssBucket;

  public void configureMessageConverters (
    List<HttpMessageConverter<?>> converters) {
    converters.add(converter());
  }

  @Bean
  public MappingJackson2HttpMessageConverter converter() {
    MappingJackson2HttpMessageConverter rv =
      new MappingJackson2HttpMessageConverter(objectMapper());
    return rv;
  }

  @Bean(name = "objectMapperForMessageConverterWeb")
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
  public OSSClient ossClient() {
    OSSClient rv = new OSSClient(
      aliyunOssEndpoint, aliyunOssAccessId, aliyunOssAccessSecret);
    return rv;
  }

  @Bean
  public UploadService uploadService() {
    UploadServiceImpl rv = new UploadServiceImpl();
    rv.setBucket(aliyunOssBucket);
    return rv;
  }
}
