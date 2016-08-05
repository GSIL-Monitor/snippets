package net.momoka.eeyore;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ResponseSpec {

  @JsonProperty("res_idfa_nohyphen")
  public boolean idfaNoHyphen;

  @JsonProperty("res_json_format")
  public String responseType;

  public ResponseSpec () {

  }
}
