package net.momoka.eeyore.http;

import java.util.Map;

public class HttpService {

  protected static RequestExecutor req = new RequestExecutor();

  public static Response get (String url) throws RequestException {
    return req.get(url, null, null);
  }

  public static Response get (
    String url,
    Map<String, String> parameters) throws RequestException {
    return req.get(url, parameters, null);
  }

  public static Response get (
    String url,
    Map<String, String> parameters,
    Map<String, String> headers) throws RequestException {
    return req.get(url, parameters, headers);
  }

  public static Response post (
    String url, Map<String, String> parameters) throws RequestException {
    return req.post(
      url, parameters, "application/x-www-form-urlencoded", null);
  }

  public static Response post (
    String url, Map<String, String> parameters, String contentType)
    throws RequestException {
    return req.post(url, parameters, contentType, null);
  }

  public static Response post (
    String url, Map<String, String> parameters,
    String contentType,
    Map<String, String> headers)
    throws RequestException {
    return req.post(url, parameters, contentType, headers);
  }

}
