package pl.hachune.models;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Person implements DataResult {

  public Person() {

  }

  @JsonProperty("name")
  private String name;

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

}
