package net.momoka.util;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class URLHelper {

  public static Map<String, String> queryDecode (String query)
    throws UnsupportedEncodingException {
    Map<String, String> rv = new TreeMap<String, String>();

    if (query == null) {
      return rv;
    }

    String[] frags = query.split("&");
    String[] _ = null;
    String key = null;
    String value = null;

    for (int i = 0; i < frags.length; i++) {
      _ = frags[i].split("=");
      key = URLDecoder.decode(_[0], "UTF-8");
      value = URLDecoder.decode(_[1], "UTF-8");
      rv.put(key, value);
    }
    return rv;
  }

  public static String queryEncode (Map<String, String> map)
    throws UnsupportedEncodingException {
    String value;

    List<String> frags = new ArrayList<String>();

    for (String key : map.keySet()) {
      value = map.get(key);
      StringBuilder sb = new StringBuilder();
      sb.append(URLEncoder.encode(key, "UTF-8"));
      sb.append("=");
      sb.append(URLEncoder.encode(value, "UTF-8"));
      frags.add(sb.toString());
    }
    return StringUtil.join("&", frags);
  }

}
