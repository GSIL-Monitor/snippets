package net.momoka.eeyore.impl;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import net.momoka.eeyore.BaseImpl;
import net.momoka.eeyore.MobileApp;
import net.momoka.eeyore.RequestSpec;
import net.momoka.eeyore.ResponseSpec;
import net.momoka.eeyore.http.HttpService;
import net.momoka.eeyore.http.RequestException;
import net.momoka.eeyore.http.Response;
import net.momoka.util.DigestUtil;
import net.momoka.util.StringUtil;
import net.momoka.util.URLHelper;

public class BaiduImeImpl implements BaseImpl {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(BaiduImeImpl.class);

  private static final String IDFA_URL =
    "http://r6.mo.baidu.com/v5/idfa/status";
  private static final String FROM = "1013684a";
  private static final String TOKEN =
    "FpOd3tLRjVaa1FBpZURPcklBQXZFNnpwM9ZrYXBoWk21";

  public byte[] sendRequest(
    MobileApp app, RequestSpec spec, List<String> idfas) {

    Response resp;
    Map<String, String> parameters = new TreeMap<String, String>();

    Long ts = System.currentTimeMillis();
    ts /= 1000;
    String timestamp = ts.toString();

    String i = StringUtil.join("\n", idfas);
    i += "\n";

    LOGGER.debug(i);

    parameters.put("from", FROM);
    parameters.put("time", timestamp);
    parameters.put("secret", getSecret(timestamp, i));

    String queryString;
    try {
      queryString = URLHelper.queryEncode(parameters);
    }
    catch (UnsupportedEncodingException e) {
      e.printStackTrace();
      return null;
    }

    LOGGER.debug("{}", parameters);

    byte[] body = i.getBytes();

    try {

      // 这里千万不能搞错，就是 text/plan ，因为很重要所以说三遍，没有看错
      // 这里千万不能搞错，就是 text/plan ，因为很重要所以说三遍，没有看错
      // 这里千万不能搞错，就是 text/plan ，因为很重要所以说三遍，没有看错
      resp = HttpService.post(
        IDFA_URL + "?" + queryString,
        null,

        "text/plan",

        null,
        body);

      if (resp.responseCode != 200) {
      LOGGER.error(
        "MobileBaidu: response error: appleId: {}, status: {}",
        Long.toString(app.appleId),
        resp.responseCode);
      }
      return resp.body;
    }
    catch (RequestException e) {
      e.printStackTrace();
      LOGGER.error(
        "MobileBaidu: request error: appleId: {}", Long.toString(app.appleId));
      return null;
    }
  }

  public Map<String, Integer> handleResponse(
    MobileApp app, ResponseSpec spec, byte[] body) {

    return null;
  }

  protected String getSecret(String timestamp, String idfas) {
    StringBuilder sb = new StringBuilder();
    sb.append(FROM);
    sb.append(timestamp);
    sb.append(TOKEN);
    sb.append(idfas);
    return DigestUtil.md5sum(sb.toString());
  }
}
