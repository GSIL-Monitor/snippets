package net.momoka.redis;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import redis.clients.jedis.Jedis;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.qianka.redis.ConnectionSpec;
import com.qianka.redis.QiankaRedis;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) throws Exception {

    QiankaRedis redis = new QiankaRedis();
    List<ConnectionSpec> specs = new ArrayList<>();
    specs.add(new ConnectionSpec("redis://127.0.0.1:6379/345", "0"));

    redis.addBind("lppa", specs);

    String key = "hello";

    Jedis jedis = redis.getBind("lppa").getClient(key);
    String _ = jedis.get("fjwifjiwf");

    LOGGER.debug("_: {}", _);

    Map<String, String> mapping = new HashMap<>();

    mapping.put("a", "1");
    mapping.put("b", "2");

    String[] values = new String[mapping.size() * 2];
    int i = 0;
    for (String k: mapping.keySet()) {
      values[i*2] = k;
      values[i*2+1] = mapping.get(k);
      i++;
    }

    LOGGER.debug("{}", values);

    _ = jedis.mset(values);

    LOGGER.debug("_: {}", _);

  }
}
