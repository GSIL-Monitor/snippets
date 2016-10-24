package net.momoka.date;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class DateUtils {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(DateUtils.class);

  public static String relativeZH(Date date) {

    Date now = new Date();
    long nowS = now.getTime();
    long dateS = date.getTime();
    long d = Math.abs(nowS - dateS);

    LOGGER.debug("{}", d);

    StringBuilder sb = new StringBuilder();

    if (d < 60000) {
      sb.append(Long.toString(d / 1000) + " 秒");
    }
    else if (d < 3600000) {
      sb.append(Long.toString(d / 60000) + " 分钟");
    }
    else if (d < 86400000) {
      sb.append(Long.toString(d / 3600000) + " 小时");
    }
    else if (d < 86400000 * 7) {
      sb.append(Long.toString(d / 86400000) + " 天");
    }
    else {
      sb.append(Long.toString(d / 86400000 / 7) + " 星期");
    }

    if (nowS >= dateS) {
      sb.append("前");
    }
    else {
      sb.append("后");
    }

    return sb.toString();

  }

}


public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main (String[] args) throws Throwable {

    Calendar now = Calendar.getInstance();

    now.add(Calendar.HOUR, -3);

    String output = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").
      format(now.getTime());

    LOGGER.debug(output);

    Thread.sleep(5000);

    LOGGER.debug(DateUtils.relativeZH(now.getTime()));

  }
}
