package net.momoka.eeyore;

import java.util.List;
import java.util.Map;

import net.momoka.eeyore.MobileApp;
import net.momoka.eeyore.RequestSpec;
import net.momoka.eeyore.ResponseSpec;
import net.momoka.eeyore.http.RequestException;

public interface BaseImpl {

  public byte[] sendRequest(
    MobileApp app, RequestSpec spec, List<String> idfas)
    throws RequestException;

  public Map<String, Integer> handleResponse(
    MobileApp app, ResponseSpec spec, byte[] body);

}
