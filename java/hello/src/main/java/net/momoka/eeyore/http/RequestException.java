package net.momoka.eeyore.http;

public class RequestException extends Throwable {

  public RequestException () {
    super();
  }

  public RequestException(String message) {
    super(message);
  }
}
