package net.momoka.jackson;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class Person {

  @JsonProperty("name_value")
  public String nameValue;

  @JsonProperty("age_value")
  public int ageValue;

}

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main (String[] args) throws Exception {

    ObjectMapper objectMapper = new ObjectMapper();

    String json = "{ \"name_value\": \"hello world\", \"age_value\": 1 }";

    Person person = objectMapper.readValue(json, Person.class);

    LOGGER.debug("name: {}", person.nameValue);
    LOGGER.debug("age: {}", Integer.toString(person.ageValue));
  }
}
