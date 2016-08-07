package net.momoka.util;

import java.util.Collection;

public class StringUtil {

  public static String join(String separator, Collection<String> coll) {
    StringBuilder sb = new StringBuilder();
    int count = 0;

    for (String s : coll) {
      if (count > 0) {
        sb.append(separator);
      }
      sb.append(s);
      count++;
    }
    return sb.toString();
  }

  public static String uuidAddHyphen(String s) {
    StringBuilder sb = new StringBuilder();
    sb.append(s.substring(0, 8));
    sb.append("-");
    sb.append(s.substring(8, 12));
    sb.append("-");
    sb.append(s.substring(12, 16));
    sb.append("-");
    sb.append(s.substring(16, 20));
    sb.append("-");
    sb.append(s.substring(20));
    return sb.toString();
  }

}
