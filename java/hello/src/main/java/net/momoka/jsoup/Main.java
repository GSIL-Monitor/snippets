package net.momoka.jsoup;

import com.qianka.util.http.HttpService;
import com.qianka.util.http.Response;
import org.jsoup.Jsoup;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) throws Exception {

    Response resp = HttpService.get("http://www.baidu.com");
    String body = resp.getBodyAsString();

    LOGGER.debug("{}", Jsoup.parse(body).text());

  }
}
