package net.momoka.eeyore.impl;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
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


class MBResponse {
  public Integer errno;
  @JsonProperty("request_id")
  public String requestId;
  public String errmsg;
  public Map<String, Integer> data;
}


public class MobileBaiduImpl implements BaseImpl {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(MobileBaiduImpl.class);


  private static final String AK = "qianka";
  // private static final String SK = "89848ec509a2c69a83b28b26c857396e";
  private static final String SK = "6ccd2782289b2a357b53358eef4eea13";
  private static final String IDFA_URL =
    "http://ext.baidu.com/api/integral/v1/idfa/query";

  protected ObjectMapper objectMapper;

  public MobileBaiduImpl() {
    objectMapper = new ObjectMapper();
    objectMapper.configure(
      DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    objectMapper.setSerializationInclusion(Include.NON_NULL);
  }

  public byte[] sendRequest(
    MobileApp app, RequestSpec spec, List<String> idfas) {

    Response resp;
    Map<String, String> parameters = new TreeMap<String, String>();

    String idfa = StringUtil.join(",", idfas);
    Long ts = System.currentTimeMillis();
    ts /= 1000;
    String timestamp = ts.toString();

    parameters.put("ak", AK);
    parameters.put("idfa", idfa);
    parameters.put("time", timestamp);

    String sign = getSign(idfa, timestamp);
    parameters.put("sign", sign);

    LOGGER.debug("{}", parameters);

    try {
      resp = HttpService.get(IDFA_URL, parameters);

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
    Map<String, Integer> rv = new TreeMap<String, Integer>();
    MBResponse resp;

    try {
      resp = objectMapper.readValue(body, MBResponse.class);

      if (resp.errno != 0) {
        String reason = "";
        try {
          reason = new String(body, "UTF-8");
        }
        catch (UnsupportedEncodingException e) {
          e.printStackTrace();
        }
        LOGGER.error(
          "MobileBaidu: handle error: appleId: {}, message: {}",
          app.appleId,
          reason);
        return rv;
      }

      rv = new TreeMap<String, Integer>(resp.data);

    }
    catch (IOException e) {
      e.printStackTrace();
      LOGGER.error(
        "MobileBaidu: handle error: appleId: {}, message: {}",
        app.appleId,
        e.getMessage());
    }

    return rv;
  }

  protected String getSign(String idfa, String timestamp) {
    StringBuilder sb = new StringBuilder();
    sb.append("ak=");
    sb.append(AK);
    sb.append("idfa=");
    sb.append(idfa);
    sb.append("time=");
    sb.append(timestamp);
    sb.append(SK);
    return DigestUtil.md5sum(sb.toString());
  }

}
