package net.momoka.http;

import java.util.Map;
import java.util.TreeMap;

import sun.net.www.http.HttpClient;

import com.qianka.util.http.HttpClientRequestExecutor;
import com.qianka.util.http.HttpService;
import com.qianka.util.http.RequestExecutor;
import com.qianka.util.http.RequestExecutorBuilder;
import com.qianka.util.http.Response;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public Main() {

  }

  public static void main(String[] args) throws Exception {
    // String url = "http://ip.cn/";

//    // HttpClient
//    RequestExecutorBuilder execBuilder = RequestExecutorBuilder.create();
//    execBuilder.setProxy("172.20.1.10", 3128);
//    execBuilder.setExecutor(RequestExecutorBuilder.Executors.UNIREST);
//    RequestExecutor exec = execBuilder.build();
//    HttpService.getInstance().setExecutor(exec);

//    Map<String, String> headers = new TreeMap<>();
//    headers.put("Accept", "*/*");

    LOGGER.debug("args: {}", args);

    String url = "http://127.0.0.1";
    if (args.length > 0) {
      url = args[0];
    }

    Response resp = HttpService.get(url);
    LOGGER.debug("{}", resp.getBodyAsString());
  }
}
