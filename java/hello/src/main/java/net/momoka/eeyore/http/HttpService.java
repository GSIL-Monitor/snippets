package net.momoka.eeyore.http;

import java.util.Map;

public class HttpService {

  public static Response get (String url) throws RequestException {
    RequestExecutor req = new RequestExecutor();
    return req.get(url, null, null);
  }

  public static Response get (
    String url,
    Map<String, String> parameters) throws RequestException {
    RequestExecutor req = new RequestExecutor();
    return req.get(url, parameters, null);
  }

  public static Response get (
    String url,
    Map<String, String> parameters,
    Map<String, String> headers) throws RequestException {
    RequestExecutor req = new RequestExecutor();
    return req.get(url, parameters, headers);
  }

  public static Response post (
    String url, Map<String, String> parameters) throws RequestException {
    RequestExecutor req = new RequestExecutor();
    return req.post(
      url, parameters, "application/x-www-form-urlencoded", null);
  }

  public static Response post (
    String url, Map<String, String> parameters, String contentType)
    throws RequestException {
    RequestExecutor req = new RequestExecutor();
    return req.post(url, parameters, contentType, null);
  }

  public static Response post (
    String url, Map<String, String> parameters,
    String contentType,
    Map<String, String> headers)
    throws RequestException {
    RequestExecutor req = new RequestExecutor();
    return req.post(url, parameters, contentType, headers);
  }

}
