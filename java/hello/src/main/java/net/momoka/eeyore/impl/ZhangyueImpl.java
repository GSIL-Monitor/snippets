package net.momoka.eeyore.impl;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.TreeMap;

import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import net.momoka.eeyore.BaseImpl;
import net.momoka.eeyore.MobileApp;
import net.momoka.eeyore.RequestSpec;
import net.momoka.eeyore.ResponseSpec;
import net.momoka.eeyore.http.HttpService;
import net.momoka.eeyore.http.RequestException;
import net.momoka.eeyore.http.Response;
import net.momoka.util.StringUtil;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


class Data {
  public Map<String, Integer> idfas;
}

class ZYResponse {
  public long code;
  public Data data;
  public String message;

  public ZYResponse () {

  }
}

public class ZhangyueImpl implements BaseImpl {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(ZhangyueImpl.class);

  private static final String APP_KEY = "0707";
  private static final String IDFA_URL = "http://59.151.93.147:9191/router";

  private ObjectMapper objectMapper;

  public ZhangyueImpl () {
    objectMapper = new ObjectMapper();
    objectMapper.configure(
      DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    objectMapper.setSerializationInclusion(Include.NON_NULL);
  }

  public byte[] sendRequest(
    MobileApp app, RequestSpec spec, List<String> idfas) {

    Response resp;
    Map<String, String> parameters = new TreeMap<String, String>();

    String i = StringUtil.join(",", idfas);

    parameters.put("appKey", APP_KEY);
    parameters.put("method", "idfa.filter");
    parameters.put("format", "json");
    parameters.put("v", "1.1");
    parameters.put("idfas", i);

    try {
      resp = HttpService.get(IDFA_URL, parameters);

      if (resp.responseCode != 200) {
        String reason = "";
        try {
          reason = new String(resp.body, "UTF-8");
        }
        catch (UnsupportedEncodingException e) {
        }

        LOGGER.error(
          "ZHANGYUE: response error, appleId: {}, status: {}, mesage: {}",
          app.appleId,
          resp.responseCode,
          reason);
        return null;
      }

      return resp.body;
    }
    catch (RequestException e) {
      e.printStackTrace();
      LOGGER.error(
        "ZHANGYUE: request error, appleId: {}, message: {}",
        app.appleId,
        e.getMessage());
      return null;
    }
  }

  public Map<String, Integer> handleResponse(
    MobileApp app, ResponseSpec spec, byte[] body) {

    Map<String, Integer> rv;
    ZYResponse resp;

    try {
      resp = objectMapper.readValue(body, ZYResponse.class);
    }
    catch (IOException e) {
      e.printStackTrace();
      LOGGER.error(
        "ZHANGYUE: handle error, appleId: {}, message: {}",
        app.appleId,
        e.getMessage());
      return null;
    }

    LOGGER.trace("{}", resp);

    if (resp.data == null || resp.data.idfas == null) {
      return null;
    }

    rv = new HashMap<String, Integer>(resp.data.idfas);

    return rv;
  }
}
