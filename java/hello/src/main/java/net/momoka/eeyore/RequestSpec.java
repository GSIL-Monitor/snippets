package net.momoka.eeyore;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.json.simple.JSONValue;
import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;

public class RequestSpec {

  @JsonProperty("template_code")
  public String templateCode;

  @JsonProperty("req_http_method")
  public String httpMethod;

  @JsonProperty("req_content_type")
  public String contentType;

  @JsonProperty("req_idfa_maxnum")
  public int maxNum;

  @JsonProperty("req_idfa_nohyphen")
  public boolean idfaNoHyphen;

  @JsonProperty("req_idfa_lowercase")
  public boolean idfaLowercase;

  @JsonProperty("shared_key")
  public String sharedKey;

  @JsonProperty("ext_field")
  public String extendedField;

  public RequestSpec () {
    this.templateCode = null;
    this.httpMethod = "POST";
    this.contentType = "";
    this.maxNum = 200;
    this.idfaNoHyphen = false;
    this.idfaLowercase = false;
    this.sharedKey = null;
    this.extendedField = null;
  }

  public JSONObject getExtendedFields () {
    JSONObject obj = new JSONObject();

    if (extendedField == null || "".equals(extendedField)) {
      return obj;
    }

    try {
      obj = (JSONObject) JSONValue.parseWithException(extendedField);
    }
    catch (ParseException e) {
      e.printStackTrace();
    }
    return obj;
  }
}
