package net.momoka.spring;

public class Greeter {

  private Hello hello;

  public Greeter (Hello hello) {
    this.hello = hello;
  }

  public String greet() {
    return hello.getMessage();
  }

}
