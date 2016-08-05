package net.momoka.unirest;

import java.io.InputStream;
import java.io.IOException;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);


  public static void main(String[] args) throws IOException, UnirestException {

    HttpResponse<InputStream> resp =
      Unirest.get(
        "http://knowing.corp.qianka.com/ops_api/idfa/verify?ad_id=40")
      .header("User-Agent", "Qianka IDFA Verifier 1.0")
      .asBinary();

    LOGGER.debug("status: {}", resp.getStatus());

    InputStream is = resp.getRawBody();
    int size = is.available();
    byte[] payload = new byte[size];

    for (int i = 0; i < size; i++) {
      payload[i] = (byte) is.read();
    }

    is.close();

    LOGGER.debug("{}", payload);
    LOGGER.debug("{}", new String(payload, "UTF-8"));

  }

}
