package pl.hachune;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Map;
import java.util.TreeMap;
import javax.annotation.Resource;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.qianka.util.http.HttpException;
import com.qianka.util.http.HttpService;
import com.qianka.util.http.Response;
import com.qianka.util.CodecUtil;
import com.qianka.util.DigestUtil;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class YuntongxunNotify {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(YuntongxunNotify.class);

  private static final SimpleDateFormat dateFormat =
    new SimpleDateFormat("yyyyMMddHHmmss");

  private static final String CONTENT_TYPE_JSON =
    "application/json";

  private String accountSid;
  private String accountToken;
  private String appId;
  private String apiBase;
  private String displayNumber;

  @Resource
  HttpService httpService;

  @Resource
  ObjectMapper objectMapper;

  public YuntongxunNotify() {

  }

  public String getAccountSid() {
    return accountSid;
  }

  public void setAccountSid(String accountSid) {
    this.accountSid = accountSid;
  }

  public String getAccountToken() {
    return accountToken;
  }

  public void setAccountToken(String accountToken) {
    this.accountToken = accountToken;
  }

  public String getAppId() {
    return appId;
  }

  public void setAppId(String appId) {
    this.appId = appId;
  }

  public String getApiBase() {
    return apiBase;
  }

  public void setApiBase(String apiBase) {
    this.apiBase = apiBase;
  }

  public String getDisplayNumber() {
    return displayNumber;
  }

  public void setDisplayNumber(String displayNumber) {
    this.displayNumber = displayNumber;
  }

  public boolean notify(String phone, String code) {
    boolean rv = false;

    Response resp = sendRequest(phone, code);
    if (resp != null) {
      rv = handleResponse(resp);
    }

    return rv;
  }

  private Response sendRequest(String phone, String code) {
    String url = null;
    Date now = null;
    Map<String, String> query = null;
    Map<String, String> headers = null;
    String payload = null;
    Response resp = null;

    YuntongxunRequestPayload request = new YuntongxunRequestPayload();
    request.setAppId(appId);
    request.setVerifyCode(code);
    request.setPlayTimes("3");
    request.setRecipient(phone);
    request.setDisplayNumber(displayNumber);

    try {
      payload = objectMapper.writeValueAsString(request);
    }
    catch (IOException e) {
      e.printStackTrace();
      LOGGER.error("error when encoding YuntongxunRequestPayload into JSON");
      return resp;
    }

    now = new Date();

    query = new TreeMap<String, String>();
    headers = new TreeMap<String, String>();

    query.put("sig", getSign(now));
    headers.put("Accept", CONTENT_TYPE_JSON);
    headers.put("Authorization", getAuthorization(now));
    url = getRequestUrl();

    LOGGER.debug("url: {}", url);
    LOGGER.debug("query: {}", query);
    LOGGER.debug("headers: {}", headers);
    LOGGER.debug("payload: {}", payload);

    try {
      resp = httpService.post(
        url, // url
        query, // query
        CONTENT_TYPE_JSON,  // contentType
        headers, // headers
        payload.getBytes()); // body
    }
    catch (HttpException e) {
      e.printStackTrace();
    }

    return resp;
  }

  private boolean handleResponse(Response resp) {
    boolean rv = false;
    int code = resp.getResponseCode();
    String body = resp.getBodyAsString();

    if (code != 200) {
      LOGGER.error("HTTP status code is not 200");
      LOGGER.error("body: {}", body);
    }

    YuntongxunResponse payload = null;

    try {
      payload = objectMapper.readValue(body, YuntongxunResponse.class);
    }
    catch (IOException e) {
      e.printStackTrace();
      LOGGER.error("error when deocoding JSON into object");
      return false;
    }

    if ("000000".equals(payload.getStatusCode())) {
      rv = true;
    }
    else {
      LOGGER.error("statusCode in payload is not 000000");
      LOGGER.error("body: {}", body);
    }

    return rv;
  }

  private String getRequestUrl() {
    StringBuilder sb = new StringBuilder();
    sb.append(apiBase).
      append("Accounts/").
      append(accountSid).
      append("/Calls/VoiceVerify");

    return sb.toString();
  }

  private String getAuthorization(Date date) {
    String t = dateFormat.format(date);

    StringBuilder sb = new StringBuilder();
    sb.append(accountSid).append(":").append(t);

    String rv = CodecUtil.base64Encode(sb.toString().getBytes());
    LOGGER.debug("authorization: {}", rv);
    return rv;
  }

  private String getSign(Date date) {
    String t = dateFormat.format(date);

    StringBuilder sb = new StringBuilder();
    sb.append(accountSid).append(accountToken).append(t);

    LOGGER.debug("sign string: {}", sb.toString());
    String rv = DigestUtil.md5sum(sb.toString()).toUpperCase();
    LOGGER.debug("sign: {}", rv);
    return rv;
  }

}
