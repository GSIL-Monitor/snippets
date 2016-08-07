package net.momoka.eeyore.impl;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.TreeMap;

import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import net.momoka.eeyore.MobileApp;
import net.momoka.eeyore.RequestSpec;
import net.momoka.eeyore.ResponseSpec;
import net.momoka.eeyore.http.HttpService;
import net.momoka.eeyore.http.RequestException;
import net.momoka.eeyore.http.Response;
import net.momoka.eeyore.BaseImpl;
import net.momoka.util.DigestUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


class Item {

  public String idfa;
  public int clientType;

  // 京东文档与接口中返回数据的key真的就是 `ativation`
  @JsonProperty("ativation")
  public Boolean activation;

  public Item () {

  }
}

class Result {

  public String code;
  public Item[] result;

}

public class JingdongImpl implements BaseImpl {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(JingdongImpl.class);

  protected static final String UNION_ID = "350268123";
  protected static final String SECRET =
    "NBQK-7J89-JKDS-RMNW-DEBC-2H8D-KH";
  protected static final String IDFA_URL =
    "http://adcollect.m.jd.com/queryAtivationByIdfa.do";


  protected ObjectMapper objectMapper;

  public JingdongImpl () {
    objectMapper = new ObjectMapper();
    objectMapper.configure(
      DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    objectMapper.setSerializationInclusion(Include.NON_NULL);
  }

  public byte[] sendRequest(
    MobileApp app, RequestSpec spec, List<String> idfas) {

    Response resp;
    byte[] rv = null;
    int clientType = 0;

    if (idfas == null || idfas.size() <= 0) {
      LOGGER.warn("JD: no idfas");
      return rv;
    }

    if (app.appleId == 414245413) {
      // 商城
      clientType = 1;
    }
    else if (app.appleId == 895682747) {
      // 金融
      clientType = 4;
    }
    else if (app.appleId == 832444218) {
      // 钱包
      clientType = 7;
    }
    else if (app.appleId == 506583396) {
      // 阅读
      clientType = 10;
    }
    else {
      LOGGER.warn("JD: unknown appleId: {}", app.appleId);
      return rv;
    }

    objectMapper.configure(
      DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    objectMapper.setSerializationInclusion(Include.NON_NULL);

    Map<String, String> parameters = new TreeMap<String, String>();

    List<Item> items = new ArrayList<Item>();

    for (String idfa: idfas) {
      Item i = new Item();
      i.idfa = idfa;
      i.clientType = clientType;
      items.add(i);
    }

    String body = "";
    try {
      body = objectMapper.writeValueAsString(items);
    }
    catch (JsonProcessingException e) {
      e.printStackTrace();
      return rv;
    }

    parameters.put("body", body);
    parameters.put("unionId", UNION_ID);
    parameters.put("sign", getSign(body));

    LOGGER.debug("{}", parameters);

    try {
      resp = HttpService.post(IDFA_URL, parameters);
    }
    catch (RequestException e) {
      e.printStackTrace();
      return null;
    }

    LOGGER.debug("status: {}", resp.responseCode);

    if (resp.responseCode != 200) {
      String reason = "";
      try {
        reason = new String(resp.body, "UTF-8");
      }
      catch  (UnsupportedEncodingException err) {
      }
      LOGGER.error(
        "JD: response code: {}, appleId: {}, url: '{}', message: '{}'",
        resp.responseCode,
        app.appleId,
        IDFA_URL,
        reason);
      return null;
    }

    try {
      Result result = objectMapper.readValue(resp.body, Result.class);
      if (result.result == null) {
        LOGGER.error(
          "JD: appleId: {}, url: '{}', jd response code: {}",
          app.appleId,
          IDFA_URL,
          result.code);
        return null;
      }
    }
    catch (IOException e) {
      e.printStackTrace();
      return null;
    }

    return resp.body;
  }

  public Map<String, Integer> handleResponse(
    MobileApp app, ResponseSpec spec, byte[] body) {

    Map<String, Integer> rv = new HashMap<String, Integer>();

    objectMapper.configure(
      DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    objectMapper.setSerializationInclusion(Include.NON_NULL);

    try {
      Result result = objectMapper.readValue(body, Result.class);

      LOGGER.debug("{}", result.result);

      for (int i = 0; i < result.result.length; i++) {
        boolean activation = result.result[i].activation;
        String idfa = result.result[i].idfa;
        if (activation) {
          rv.put(idfa, 1);
        }
        else {
          rv.put(idfa, 0);
        }
      }
    }
    catch (IOException e) {
      e.printStackTrace();
      return rv;
    }

    return rv;
  }

  protected String getSign(String body) {
    StringBuilder sb = new StringBuilder();
    sb.append(body);
    sb.append(SECRET);
    return DigestUtil.md5sum(sb.toString()).toUpperCase();
  }
}
