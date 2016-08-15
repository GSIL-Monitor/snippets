package net.momoka.httpclient;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);


  public static void main(String[] args)
    throws IOException, URISyntaxException {

    URI u = new URI("http://knowing.corp.qianka.com/ops_api/notify");

    URIBuilder ub = new URIBuilder(u);
    ub.addParameter("title", "test");
    ub.addParameter("message", "just a test");
    u = ub.build();

    LOGGER.debug("{}", u);

    CloseableHttpClient httpclient = HttpClients.createDefault();
    HttpGet get = new HttpGet(u);
    CloseableHttpResponse resp = httpclient.execute(get);

    int status = resp.getStatusLine().getStatusCode();
    LOGGER.debug("status: {}", status);
    String body = "";
    if (status == 200){

      try {
        HttpEntity entity = resp.getEntity();
        long contentLength = entity.getContentLength();
        LOGGER.debug("Content-Length: {}", contentLength);
        body = EntityUtils.toString(entity);
      }
      finally {
        resp.close();
      }
      LOGGER.debug("{}", body);
    }

  }

}
