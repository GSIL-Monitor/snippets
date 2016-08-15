package net.momoka.spring.model;


public class User {
  private long id;
  private String username;

  public void setId(long id) {
    this.id = id;
  }

  public void setUsername(String username) {
    this.username = username;
  }

  public long getId() {
    return this.id;
  }

  public String getUsername() {
    return this.username;
  }

  public String toString() {
    return String.format("<#User #%d:%s>", this.id, this.username);
  }

}
