package net.momoka.util;

import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class DigestUtil {

  public static String md5sum (String payload) {
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

}
