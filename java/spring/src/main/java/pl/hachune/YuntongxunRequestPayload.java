package pl.hachune;

import com.fasterxml.jackson.annotation.JsonProperty;

public class YuntongxunRequestPayload {

  public YuntongxunRequestPayload() {

  }

  @JsonProperty("appId")
  private String appId;

  @JsonProperty("verifyCode")
  private String verifyCode;

  @JsonProperty("playTimes")
  private String playTimes;

  @JsonProperty("to")
  private String recipient;

  @JsonProperty("displayNum")
  private String displayNumber;

  public String getAppId() {
    return appId;
  }

  public void setAppId(String appId) {
    this.appId = appId;
  }

  public String getVerifyCode() {
    return verifyCode;
  }

  public void setVerifyCode(String verifyCode) {
    this.verifyCode = verifyCode;
  }

  public String getPlayTimes() {
    return playTimes;
  }

  public void setPlayTimes(String playTimes) {
    this.playTimes = playTimes;
  }

  public String getRecipient() {
    return recipient;
  }

  public void setRecipient(String recipient) {
    this.recipient = recipient;
  }

  public String getDisplayNumber() {
    return displayNumber;
  }

  public void setDisplayNumber(String displayNumber) {
    this.displayNumber = displayNumber;
  }

}
