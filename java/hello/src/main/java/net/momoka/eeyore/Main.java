package net.momoka.eeyore;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import net.momoka.eeyore.impl.BaiduImeImpl;
import net.momoka.eeyore.impl.JingdongImpl;
import net.momoka.eeyore.impl.MobileBaiduImpl;
import net.momoka.eeyore.impl.ZhangyueImpl;
import net.momoka.eeyore.http.RequestException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main (String[] args)
    throws RequestException, UnsupportedEncodingException {

    // BaseImpl impl = new BaiduImeImpl();
    // BaseImpl impl = new JingdongImpl();
    BaseImpl impl = new MobileBaiduImpl();
    // BaseImpl impl = new ZhangyueImpl();
    MobileApp app = new MobileApp();
    // app.appleId = 414245413;

    RequestSpec reqSpec = new RequestSpec();

    List<String> idfas = new ArrayList<String>();

    for (int i = 0; i < 10; i++) {
      idfas.add(UUID.randomUUID().toString().toUpperCase());
    }

    LOGGER.debug("{}", idfas);

    byte[] body = impl.sendRequest(app, reqSpec, idfas);

    LOGGER.debug("{}", body);
    if (body == null) {
      return;
    }

    LOGGER.debug("{}", new String(body, "UTF-8"));

    ResponseSpec respSpec = new ResponseSpec();
    Map<String, Integer> result =
      impl.handleResponse(app, respSpec, body);

    LOGGER.debug("{}", result);
  }

}
