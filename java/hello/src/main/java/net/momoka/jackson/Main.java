package net.momoka.jackson;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.PropertyNamingStrategy;
import com.fasterxml.jackson.databind.SerializationFeature;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class Person {

  @JsonProperty("name_value2")
  private String nameValue;

  @JsonProperty("age_value2")
  private int ageValue;

  public String getNameValue() {
    return nameValue;
  }

  public void setNameValue(String v) {
    nameValue = v;
  }

  public int getAgeValue() {
    return ageValue;
  }

  public void setAgeValue(int v) {
    ageValue = v;
  }

}

class Response {

  @JsonProperty("code")
  private Integer code;

  @JsonProperty("list")
  private Map<String, Long> idfas;

  public Integer getCode() {
    return code;
  }

  public void setCode(Integer v) {
    code = v;
  }

  public Map<String, Long> getIdfas() {
    return idfas;
  }

  public void setIdfas(Map<String, Long> v) {
    idfas = v;
  }

}

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main (String[] args) throws Exception {

    ObjectMapper objectMapper = new ObjectMapper();

    objectMapper.configure(
      DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    objectMapper.configure(
      SerializationFeature.WRITE_NULL_MAP_VALUES, false);
    objectMapper.setSerializationInclusion(Include.NON_NULL);
    objectMapper.setPropertyNamingStrategy(
      PropertyNamingStrategy.SNAKE_CASE);

    String json = "{ \"name_value2\": \"hello world\", \"age_value2\": 1 }";

    Person person = objectMapper.readValue(json, Person.class);

    LOGGER.debug("name: {}", person.getNameValue());
    LOGGER.debug("age: {}", person.getAgeValue());

    List<Integer> numbers = new ArrayList<Integer>();
    numbers.add(10);
    numbers.add(3);

    String _ = objectMapper.writeValueAsString(numbers);
    LOGGER.debug(_);

    Person p2 = new Person();
    p2.setNameValue("person2");
    p2.setAgeValue(2222);
    _ = objectMapper.writeValueAsString(p2);
    LOGGER.debug(_);

    String in = "{\"code\":0,\"list\":{\"5A0620B7-9291-4AB2-8418-CFB51D646CBF\":0,\"DB24DCC5-EC5C-495B-8EEC-87CF02BEAE90\":0,\"B8251CE1-AB2F-47E3-A452-10C958015681\":0,\"3048B94D-6D63-468B-8A39-7B40830B36A6\":0,\"FB6AB631-59DD-4499-9668-E1FA528DDA29\":0,\"FC7F6368-E2F2-483D-8228-3F7E708D34E7\":0,\"F2CC584D-638E-4955-BC82-77874B18ED0B\":0,\"8A754547-C233-4D75-9642-3255B0F787A2\":0,\"2007A7CE-D245-4281-A462-9557157FEAB0\":0,\"AFF4ED39-7BF9-421D-BF8D-7B8564DB2B54\":0}}";


    Response resp = objectMapper.readValue(in, Response.class);
    LOGGER.debug("{}", resp.getIdfas());

  }
}
