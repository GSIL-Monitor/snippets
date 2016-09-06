package net.momoka.httpclient;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.Map;
import java.util.TreeMap;

import org.apache.http.util.EntityUtils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);


  public static void main(String[] args)
    throws Exception {

    // URI u = new URI("http://knowing.corp.qianka.com/ops_api/notify");
    // String url = "http://guest:guest@n1413.ops.gaoshou.me:15672/api/"
    //   + "queues/%2f/notify.chenlei.test.urgent/bindings";

    String url = "https://channel.do.baidu.com:8443/idfa/"
      + "baiduwaimai/compareIdfa";

    RequestExecutor ex = new RequestExecutor();
    Response resp = ex.get(url, null, null);
    LOGGER.debug(resp.getBodyAsString());

    // url = "http://127.0.0.1:9292/post";
    // Map<String, String> params = new TreeMap<String, String>();
    // params.put("a", "1");
    // params.put("b", "2");
    //
    // resp = ex.post(url, params, null, null);
    // LOGGER.debug(resp.getBodyAsString());
    //
    // url = "http://127.0.0.1:9292/post-body";
    // resp = ex.post(url, "just a message to test", null, null);
    // LOGGER.debug(resp.getBodyAsString());
  }

}
