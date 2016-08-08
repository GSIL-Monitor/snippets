package net.momoka.eeyore.http;

import java.io.InputStream;
import java.io.IOException;
import java.util.Map;
import java.util.HashMap;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import com.mashape.unirest.request.HttpRequest;
import com.mashape.unirest.request.HttpRequestWithBody;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;



public class RequestExecutor {
  private static final Logger LOGGER =
    LoggerFactory.getLogger(RequestExecutor.class);

  private static final String USER_AGENT = "Qianka Eeyore Verifier 1.0";
  private int connectTimeout = 5000;
  private int readTimeout = 30000;

  public RequestExecutor () {
    Unirest.setTimeouts(connectTimeout, readTimeout);
  }

  public Response get (
    String url,
    Map<String, String> parameters,
    Map<String, String> headers) throws RequestException {

    Response rv = new Response();

    HttpRequest req = Unirest.get(url);

    if (parameters != null) {
      Map<String, Object> t = new HashMap<String, Object>(parameters);
      req.queryString(t);
    }

    if (headers != null) {
      req.headers(headers);
    }
    req.header("User-Agent", USER_AGENT);
    try {
      HttpResponse<InputStream> resp = req.asBinary();
      InputStream is = resp.getRawBody();
      int size = is.available();
      byte[] payload = new byte[size];

      for (int i = 0; i < size; i++) {
        payload[i] = (byte) is.read();
      }
      is.close();

      rv.responseCode = resp.getStatus();
      rv.body = payload;
    }
    catch (UnirestException e) {
      e.printStackTrace();
      RequestException err = new RequestException(e.getMessage());
      throw err;
    }
    catch (IOException e) {
      e.printStackTrace();
      RequestException err = new RequestException(e.getMessage());
      throw err;
    }

    return rv;
  }


  public Response post (
    String url, Map<String, String> parameters,
    String contentType, Map<String, String> headers,
    byte[] body)
    throws RequestException {

    Response rv = new Response();

    LOGGER.debug("{}", url);

    HttpRequestWithBody req = Unirest.post(url);

    if (parameters != null) {
      Map<String, Object> t = new HashMap<String, Object>(parameters);
      req.fields(t);
    }

    if (body != null) {
      req.body(body);
    }

    if (headers != null) {
      req.headers(headers);
    }
    req.header("Content-Type", contentType);
    req.header("User-Agent", USER_AGENT);

    try {
      HttpResponse<InputStream> resp = req.asBinary();

      int status = resp.getStatus();
      rv.responseCode = status;

      InputStream is = resp.getRawBody();
      int size = is.available();
      byte[] payload = new byte[size];

      for (int i = 0; i < size; i++) {
        payload[i] = (byte) is.read();
      }
      is.close();
      rv.body = payload;
    }
    catch (UnirestException e) {
      e.printStackTrace();
      RequestException err = new RequestException(e.getMessage());
      throw err;
    }
    catch (IOException e) {
      e.printStackTrace();
      RequestException err = new RequestException(e.getMessage());
      throw err;
    }

    return rv;
  }
}
