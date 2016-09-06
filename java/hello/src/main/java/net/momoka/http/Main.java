package net.momoka.http;

import com.qianka.util.http.HttpService;
import com.qianka.util.http.Response;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public Main() {

  }

  public static void main(String[] args) throws Exception {
    HttpService.setExecutor(HttpService.Executor.HTTPCLIENT);

    String url = "https://channel.do.baidu.com:8443/idfa/"
      + "baiduwaimai/compareIdfa";

    Response resp = HttpService.get(url);
    LOGGER.debug("{}", resp.getBodyAsString());
  }
}
