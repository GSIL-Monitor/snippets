package net.momoka.httpclient;

import java.io.IOException;
import java.io.ByteArrayOutputStream;
import java.io.UnsupportedEncodingException;
import java.net.URI;
import java.net.URISyntaxException;
import java.security.KeyManagementException;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.http.NameValuePair;
import org.apache.http.HttpEntity;
import org.apache.http.HttpHost;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpEntityEnclosingRequestBase;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.config.Registry;
import org.apache.http.config.RegistryBuilder;
import org.apache.http.conn.socket.ConnectionSocketFactory;
import org.apache.http.conn.socket.PlainConnectionSocketFactory;
import org.apache.http.conn.ssl.NoopHostnameVerifier;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.conn.ssl.TrustSelfSignedStrategy;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.impl.conn.PoolingHttpClientConnectionManager;
import org.apache.http.message.AbstractHttpMessage;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.ssl.SSLContextBuilder;
import org.apache.http.ssl.SSLContexts;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class RequestExecutor {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(RequestExecutor.class);

  protected static final String USER_AGENT = "Qianka HttpClient 1.0";

	protected static final int CONNECTION_TIMEOUT = 5000;
	protected static final int SOCKET_TIMEOUT = 30000;
	protected static final int MAX_TOTAL = 200;
	protected static final int MAX_PER_ROUTE = 20;

  protected CloseableHttpClient httpClient;

  public RequestExecutor()
    throws NoSuchAlgorithmException,
           KeyManagementException,
           KeyStoreException {
    HttpHost proxy = null;

    KeyStore trustStore = KeyStore.getInstance(KeyStore.getDefaultType());

    SSLContextBuilder sslCtxBuilder = SSLContexts.custom().
      loadTrustMaterial(trustStore, new TrustSelfSignedStrategy());
    SSLConnectionSocketFactory sslSocketFactory =
      new SSLConnectionSocketFactory(
        sslCtxBuilder.build()); // , NoopHostnameVerifier.INSTANCE);

    Registry<ConnectionSocketFactory> registry =
      RegistryBuilder.<ConnectionSocketFactory>create().
      register("https", sslSocketFactory).
      register("http", PlainConnectionSocketFactory.INSTANCE).
      build();

    PoolingHttpClientConnectionManager connectionManager =
      new PoolingHttpClientConnectionManager(registry);
    connectionManager.setMaxTotal(MAX_TOTAL);
    connectionManager.setDefaultMaxPerRoute(MAX_PER_ROUTE);


    RequestConfig config = RequestConfig.custom().
      setConnectTimeout(CONNECTION_TIMEOUT).
      setSocketTimeout(SOCKET_TIMEOUT).
      setConnectionRequestTimeout(SOCKET_TIMEOUT).
      setProxy(proxy).
      build();

    httpClient = HttpClientBuilder.create().
      setDefaultRequestConfig(config).
      disableRedirectHandling().
      setConnectionManager(connectionManager).
      build();
  }

  public Response get(
    String url,
    Map<String, String> query,
    Map<String, String> headers) throws HttpException {
    try {
      return _get(url, query, headers);
    }
    catch(IOException e) {
      HttpException ex = new HttpException(e.getMessage());
      ex.setStackTrace(e.getStackTrace());
      throw ex;
    }
    catch(URISyntaxException e) {
      HttpException ex = new HttpException(e.getMessage());
      ex.setStackTrace(e.getStackTrace());
      throw ex;
    }
  }

  public Response post(
    String url,
    Map<String, String> parameters,
    Map<String, String> query,
    Map<String, String> headers)
    throws HttpException {
    try {
      return _post(url, parameters, query, headers);
    }
    catch(IOException e) {
      HttpException ex = new HttpException(e.getMessage());
      ex.setStackTrace(e.getStackTrace());
      throw ex;
    }
    catch(URISyntaxException e) {
      HttpException ex = new HttpException(e.getMessage());
      ex.setStackTrace(e.getStackTrace());
      throw ex;
    }
  }

  public Response post(
    String url,
    byte[] body,
    Map<String, String> query,
    Map<String, String> headers)
    throws HttpException {
    try {
      return _post(url, body, query, headers);
    }
    catch(IOException e) {
      HttpException ex = new HttpException(e.getMessage());
      ex.setStackTrace(e.getStackTrace());
      throw ex;
    }
    catch(URISyntaxException e) {
      HttpException ex = new HttpException(e.getMessage());
      ex.setStackTrace(e.getStackTrace());
      throw ex;
    }
  }

  public Response post(
    String url,
    String body,
    Map<String, String> query,
    Map<String, String> headers)
    throws HttpException {
    try {
      return _post(url, body.getBytes(), query, headers);
    }
    catch(IOException e) {
      HttpException ex = new HttpException(e.getMessage());
      ex.setStackTrace(e.getStackTrace());
      throw ex;
    }
    catch(URISyntaxException e) {
      HttpException ex = new HttpException(e.getMessage());
      ex.setStackTrace(e.getStackTrace());
      throw ex;
    }
  }

  protected Response _get(
    String url,
    Map<String, String> query,
    Map<String, String> headers)
    throws IOException, URISyntaxException {

    URIBuilder ub = new URIBuilder(url);
    processQuery(ub, query);

    HttpGet method = new HttpGet(ub.build());
    processHeader(method, headers);

    CloseableHttpResponse resp = httpClient.execute(method);
    return processResponse(resp);
  }

  protected Response _post(
    String url,
    Map<String, String> parameters,
    Map<String, String> query,
    Map<String, String> headers)
    throws IOException, URISyntaxException {

    URIBuilder ub = new URIBuilder(url);
    processQuery(ub, query);

    HttpPost method = new HttpPost(ub.build());
    processHeader(method, headers);
    processParameter(method, parameters);

    CloseableHttpResponse resp = httpClient.execute(method);
    return processResponse(resp);
  }

  protected Response _post(
    String url,
    byte[] body,
    Map<String, String> query,
    Map<String, String> headers)
    throws IOException, URISyntaxException {

    URIBuilder ub = new URIBuilder(url);
    processQuery(ub, query);

    HttpPost method = new HttpPost(ub.build());
    processHeader(method, headers);

    ByteArrayEntity e = new ByteArrayEntity(body);
    method.setEntity(e);

    CloseableHttpResponse resp = httpClient.execute(method);
    return processResponse(resp);
  }

  protected void processQuery(URIBuilder ub, Map<String, String> query) {
    if (query != null) {
      for(String key : query.keySet()) {
        String value = query.get(key);
        ub.addParameter(key, value);
      }
    }
  }

  protected void processHeader(
    AbstractHttpMessage method, Map<String, String> headers) {
    method.setHeader("User-Agent", USER_AGENT);
    if (headers != null) {
      for(String key: headers.keySet()) {
        String value = headers.get(key);
        method.setHeader(key, value);
      }
    }
  }

  protected void processParameter(
    HttpEntityEnclosingRequestBase method,
    Map<String, String> parameters) throws UnsupportedEncodingException {
    if (parameters != null) {
      List<NameValuePair> pairs = new ArrayList<NameValuePair>();
      for (String key : parameters.keySet()) {
        String value = parameters.get(key);
        pairs.add(new BasicNameValuePair(key, value));
      }
      method.setEntity(new UrlEncodedFormEntity(pairs));
    }
  }

  protected Response processResponse(CloseableHttpResponse resp)
    throws IOException {
    int status = resp.getStatusLine().getStatusCode();
    ByteArrayOutputStream bs = new ByteArrayOutputStream();
    HttpEntity en = resp.getEntity();
    en.writeTo(bs);
    byte[] b = bs.toByteArray();
    resp.close();

    Response rv = new Response();
    rv.setResponseCode(status);
    rv.setBody(b);
    return rv;
  }

}
