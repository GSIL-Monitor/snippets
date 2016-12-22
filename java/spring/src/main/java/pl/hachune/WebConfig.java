package pl.hachune;

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
import org.springframework.context.annotation.FilterType;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.annotation.PropertySources;
import org.springframework.http.MediaType;
import org.springframework.http.converter.ByteArrayHttpMessageConverter;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.converter.json
  .MappingJackson2HttpMessageConverter;
import org.springframework.http.converter.ResourceHttpMessageConverter;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.http.converter.support.
  AllEncompassingFormHttpMessageConverter;
import org.springframework.http.converter.xml.SourceHttpMessageConverter;
import org.springframework.stereotype.Controller;
import org.springframework.web.servlet.config.annotation.
  ContentNegotiationConfigurer;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.
  WebMvcConfigurerAdapter;
import org.springframework.web.servlet.view.freemarker.
  FreeMarkerConfigurer;
import org.springframework.web.servlet.view.freemarker.
  FreeMarkerViewResolver;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@EnableWebMvc
@Configuration
@PropertySources(
  value={@PropertySource("classpath:config.properties"),
         @PropertySource(value="file:${config}",
                         ignoreResourceNotFound=true)}
)
@ComponentScan(
  basePackages="pl.hachune.controllers"
)
public class WebConfig extends WebMvcConfigurerAdapter {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(WebConfig.class);

  public void configureContentNegotiation(
    ContentNegotiationConfigurer configurer) {

    configurer.favorPathExtension(true).
      favorParameter(false).
      ignoreAcceptHeader(false).
      useJaf(false).
      defaultContentType(MediaType.APPLICATION_JSON).
      mediaType("xml", MediaType.APPLICATION_XML).
      mediaType("json", MediaType.APPLICATION_JSON);

  }

  public void configureMessageConverters (
    List<HttpMessageConverter<?>> converters) {

		StringHttpMessageConverter stringConverter =
      new StringHttpMessageConverter();
		stringConverter.setWriteAcceptCharset(false);

		converters.add(new ByteArrayHttpMessageConverter());
		converters.add(stringConverter);
		converters.add(new ResourceHttpMessageConverter());
		converters.add(new SourceHttpMessageConverter<>());
		converters.add(new AllEncompassingFormHttpMessageConverter());
    converters.add(converter());

    LOGGER.debug("{}", converters);
    super.configureMessageConverters(converters);
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
  public FreeMarkerConfigurer freemarkerConfig() {
    FreeMarkerConfigurer rv = new FreeMarkerConfigurer();
    rv.setTemplateLoaderPath("classpath:pl/hachune/templates/");
    return rv;
  }

  @Bean
  public FreeMarkerViewResolver viewResolver() {
    FreeMarkerViewResolver rv = new FreeMarkerViewResolver();
    rv.setCache(true);
    rv.setPrefix("");
    rv.setSuffix(".ftl");
    rv.setContentType("text/html;charset=UTF-8");
    return rv;
  }

}
