package net.momoka;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;

public class APIResult {

  @JsonProperty("status")
  private String status;

  @JsonProperty("err_msg")
  private String errorMessage;

  @JsonProperty("data")
  private List<DataResult> data;

  public String getStatus() {
    return status;
  }

  public void setStatus(String status) {
    this.status = status;
  }

  public String getErrorMessage() {
    return errorMessage;
  }

  public void setErrorMessage(String errorMessage) {
    this.errorMessage = errorMessage;
  }

  public List<DataResult> getData() {
    return data;
  }

  public void setData(List<DataResult> data) {
    this.data = data;
  }

}
