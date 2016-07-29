package net.momoka.urlconnection;

import java.io.BufferedInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.net.URLDecoder;
import java.util.Arrays;
import java.util.Collection;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


class RequestException extends Throwable {

  public RequestException () {
    super();
  }

  public RequestException(String message) {
    super(message);
  }

}

class URLHelper {

  public static Map<String, String> queryDecode (String query)
    throws UnsupportedEncodingException {
    Map<String, String> rv = new TreeMap<String, String>();
    String[] frags = query.split("&");
    String[] _ = null;
    String key = null;
    String value = null;

    for (int i = 0; i < frags.length; i++) {
      _ = frags[i].split("=");
      key = URLDecoder.decode(_[0], "UTF-8");
      value = URLDecoder.decode(_[1], "UTF-8");
      rv.put(key, value);
    }
    return rv;
  }

  public static String queryEncode (Map<String, String> map)
    throws UnsupportedEncodingException {
    String value;

    List<String> frags = new ArrayList<String>();

    for (String key : map.keySet()) {
      value = map.get(key);
      StringBuilder sb = new StringBuilder();
      sb.append(URLEncoder.encode(key, "UTF-8"));
      sb.append("=");
      sb.append(URLEncoder.encode(value, "UTF-8"));
      frags.add(sb.toString());
    }
    return StringUtil.join("&", frags);
  }

}

class StringUtil {

  public static String join(String separator, Collection<String> coll) {
    StringBuilder sb = new StringBuilder();
    int count = 0;

    for (String s : coll) {
      if (count > 0) {
        sb.append(separator);
      }
      sb.append(s);
      count++;
    }
    return sb.toString();
  }
}

class Response {
  public int responseCode;
  public byte[] body;

  public Response () {

  }
}

class Request {
  private static final Logger LOGGER =
    LoggerFactory.getLogger(Request.class);

  private static final String USER_AGENT = "Qianka Eeyore Verifier 1.0";
  private int connectTimeout = 5000;
  private int readTimeout = 30000;
  private URLConnection conn = null;

  public Request () {

  }

  protected byte[] readResponse (int contentLength)
    throws SocketException {
    byte[] databuffer = new byte[contentLength];
    int writeoff = 0;
    InputStream is = null;
    BufferedInputStream bis = null;

    try {
      is = conn.getInputStream();
      bis = new BufferedInputStream(is);

      while (writeoff < contentLength) {
        if (bis.available() > 0) {
          int b = bis.read();

          if (b > 0) {
            databuffer[writeoff++] = (byte) b;
          }
          else {
            // b == -1 => EOF
            LOGGER.warn("Server sent premature EOF, aborting...");
            throw new SocketException("Unexpected EOF from server");
          }
        }
        else {

        }
      }
    }
    catch (Exception e) {
      writeoff = 0;
      Arrays.fill(databuffer, (byte) 0);
    }
    finally {
      try { bis.close(); } catch (Exception e2) {}
      try { is.close(); } catch (Exception e2) {}
    }

    if (writeoff != contentLength) {
      throw new SocketException("Request is incompleted");
    }

    return databuffer;
  }

  protected void checkContentLength() throws SocketException {
    int tempLength = conn.getContentLength();

    if (tempLength < 0) {
      LOGGER.warn(
        "Request host did not send Content-Length, abort transfer ({})",
        conn);
      throw new SocketException("missing content-length header");
    }
  }

  public Response get (String url)
    throws RequestException {
    Response rv = new Response();
    int tempLength = 0;
    try {
      URI source = new URI(url);

      conn = source.toURL().openConnection();
      conn.setConnectTimeout(connectTimeout);
      conn.setReadTimeout(readTimeout);
      conn.setRequestProperty(
        "User-Agent", USER_AGENT);

      conn.setRequestProperty("Accept", "*/*");

      conn.connect();
      checkContentLength();
      tempLength = conn.getContentLength();

      byte[] body = readResponse(tempLength);

      rv.responseCode = ((HttpURLConnection) conn).getResponseCode();
      rv.body = body;
    }
    catch (Exception e) {
      RequestException err = new RequestException(e.getMessage());
      err.setStackTrace(e.getStackTrace());
      throw err;
    }
    return rv;
  }

  public Response post (
    String url, Map<String, String> parameters,
    String contentType, Map<String, String> headers)
    throws RequestException {

    Response rv = new Response();
    String data = "";
    byte[] postdata = null;
    StringBuilder _data = new StringBuilder();
    int contentLenght = 0;
    int tempLength = 0;

    try {
      data = URLHelper.queryEncode(parameters);
      postdata = data.getBytes("UTF-8");
      contentLenght = postdata.length;

      URI source = new URI(url);

      conn = source.toURL().openConnection();
      conn.setDoOutput(true);
      ((HttpURLConnection) conn).setInstanceFollowRedirects(false);
      ((HttpURLConnection) conn).setRequestMethod("POST");

      conn.setRequestProperty(
        "Content-Type", contentType);
      conn.setRequestProperty(
        "Content-Length", Integer.toString(contentLenght));
      conn.setUseCaches(false);
      conn.setConnectTimeout(connectTimeout);
      conn.setReadTimeout(readTimeout);
      conn.setRequestProperty(
        "User-Agent", USER_AGENT);
      conn.setRequestProperty("Accept", "*/*");

      if (headers != null) {
        String value;
        for (String key : headers.keySet()) {
          value = headers.get(key);
          conn.setRequestProperty(key, value);
        }
      }

      OutputStream os = conn.getOutputStream();
      os.write(postdata);
      os.flush();

      conn.connect();
      checkContentLength();
      tempLength = conn.getContentLength();

      byte[] body = readResponse(tempLength);

      rv.responseCode = ((HttpURLConnection) conn).getResponseCode();

      rv.body = body;
    }
    catch (Exception e) {
      RequestException err = new RequestException(e.getMessage());
      err.setStackTrace(e.getStackTrace());
      throw err;
    }
    return rv;
  }
}

class HTTPService {

  public static Response get (String url) throws RequestException {
    Request req = new Request();
    return req.get(url);
  }

  public static Response post (
    String url, Map<String, String> parameters) throws RequestException {
    Request req = new Request();
    return req.post(url, parameters, "application/x-www-form-urlencoded", null);
  }

  public static Response post (
    String url, Map<String, String> parameters, String contentType)
    throws RequestException {
    Request req = new Request();
    return req.post(url, parameters, contentType, null);
  }

  public static Response post (
    String url, Map<String, String> parameters,
    String contentType,
    Map<String, String> headers)
    throws RequestException {
    Request req = new Request();
    return req.post(url, parameters, contentType, headers);
  }

}

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main (String[] args) throws Throwable {

    URI u = new URI(
      "http://guest:guest@n1416.ops.gaoshou.me:15672/hello?query=1");

    LOGGER.debug("scheme: {}", u.getScheme());
    LOGGER.debug("host: {}", u.getHost());
    LOGGER.debug("port: {}", Integer.toString(u.getPort()));
    LOGGER.debug("authority: {}", u.getAuthority());
    LOGGER.debug("userInfo: {}", u.getUserInfo());
    LOGGER.debug("path: {}", u.getPath());
    LOGGER.debug("query: {}", u.getQuery());
    LOGGER.debug("fragment: {}", u.getFragment());

    Map<String, String> query = URLHelper.queryDecode(u.getQuery());
    LOGGER.debug("{}", query.toString());
    query.put("hello", "world");
    query.put("chen", "lei");
    String q = URLHelper.queryEncode(query);
    LOGGER.debug(q);

    URI uri = new URI(
      u.getScheme(),
      null,
      u.getHost(),
      u.getPort(),
      u.getPath(),
      q,
      u.getFragment());
    LOGGER.debug(uri.toString());
    LOGGER.debug(uri.toURL().toString());

    Response resp = HTTPService.get("http://127.0.0.1/proxy.pac");

    if (resp.responseCode == HttpURLConnection.HTTP_OK) {
      LOGGER.debug("{}", new String(resp.body, "UTF-8"));
    }
    else {
      LOGGER.warn("HTTP status: {}", Integer.toString(resp.responseCode));
    }

    Map<String, String> parameters = new HashMap<String, String>();
    parameters.put("hello", "world");
    resp = HTTPService.post("http://127.0.0.1:9292/post", parameters);

    if (resp.responseCode == HttpURLConnection.HTTP_OK) {
      LOGGER.debug("{}", new String(resp.body, "UTF-8"));
    }
    else {
      LOGGER.warn("HTTP status: {}", Integer.toString(resp.responseCode));
    }

  }
}
