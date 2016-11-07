package net.momoka;

import com.fasterxml.jackson.annotation.JsonProperty;

public class UploadResult implements DataResult {

  @JsonProperty("filename")
  private String filename;

  @JsonProperty("height")
  private int height;

  @JsonProperty("width")
  private int width;

  @JsonProperty("format")
  private String format;

  public String getFilename() {
    return filename;
  }

  public void setFilename(String filename) {
    this.filename = filename;
  }

  public int getHeight() {
    return height;
  }

  public void setHeight(int height) {
    this.height = height;
  }

  public int getWidth() {
    return width;
  }

  public void setWidth(int width) {
    this.width = width;
  }

  public String getFormat() {
    return format;
  }

  public void setFormat(String format) {
    this.format = format;
  }

}
