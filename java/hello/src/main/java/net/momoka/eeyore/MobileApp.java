package net.momoka.eeyore;

public class MobileApp {

  public long advertiserId;
  public long appleId;
  public String idfaUrl;
  public String title;
  public int idfaType;

  public MobileApp () {

  }

  public long getAppleId () {
    return this.appleId;
  }

  public String getTitle () {
    return this.title;
  }
}
