package pl.hachune;

import com.fasterxml.jackson.annotation.JsonProperty;

public class YuntongxunResponse {

  public YuntongxunResponse() {

  }

  @JsonProperty("statusCode")
  private String statusCode;

  @JsonProperty("callSid")
  private String callSid;

  @JsonProperty("dateCreated")
  private String dateCreated;

  public String getStatusCode() {
    return statusCode;
  }

  public void setStatusCode(String statusCode) {
    this.statusCode = statusCode;
  }

  public String getCallSid() {
    return callSid;
  }

  public void setCallSid(String callSid) {
    this.callSid = callSid;
  }

  public String getDateCreated() {
    return dateCreated;
  }

  public void setDateCreated(String dateCreated) {
    this.dateCreated = dateCreated;
  }

}
