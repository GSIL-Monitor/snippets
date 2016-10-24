package net.momoka;

import com.fasterxml.jackson.annotation.JsonProperty;

public class UploadResult {

  // @JsonProperty("status")
  private String status;

  // @JsonProperty("err_msg")
  private String errorMessage;

  // @JsonProperty("filename")
  private String filename;

  // @JsonProperty("bucket")
  private String bucket;

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

  public String getFilename() {
    return filename;
  }

  public void setFilename(String filename) {
    this.filename = filename;
  }

  public String getBucket() {
    return bucket;
  }

  public void setBucket(String bucket) {
    this.bucket = bucket;
  }

}
