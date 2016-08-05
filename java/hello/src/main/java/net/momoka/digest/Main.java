package net.momoka.digest;

import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  private static String getMd5(String payload) {
    String rv = "";

    try {
      byte[] b = payload.getBytes("UTF-8");
      MessageDigest md5 = MessageDigest.getInstance("MD5");
      byte[] hash = md5.digest(b);
      rv = String.format("%032x", new BigInteger(1, hash));
    }
    catch (UnsupportedEncodingException e) {
      e.printStackTrace();
    }
    catch (NoSuchAlgorithmException e) {
      e.printStackTrace();
    }

    return rv;
  }

  public static void main (String[] args) {

    LOGGER.debug("{}", getMd5("123456"));
    LOGGER.debug("{}", getMd5("123456"));

  }

}
