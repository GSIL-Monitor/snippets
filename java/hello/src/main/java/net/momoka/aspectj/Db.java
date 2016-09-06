package net.momoka.aspectj;

public class Db {

  public Db() {

  }

  public String getSomething() {
    try {
      Thread.sleep(2000);
    }
    catch (InterruptedException e) {
    }
    return "Hello, World";
  }

}
