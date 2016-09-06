package net.momoka.httpclient;

public class Response {

  protected int responseCode;
  protected byte[] body;

  public void setResponseCode(int c) {
    this.responseCode = c;
  }

  public void setBody(byte[] b) {
    this.body = b;
  }

  public byte[] getBody() {
    return body;
  }

  public int getResponseCode() {
    return responseCode;
  }

  public String getBodyAsString() {
    return new String(body);
  }

}
