package net.momoka.eeyore;

import java.util.List;
import java.util.Map;

import net.momoka.eeyore.MobileApp;
import net.momoka.eeyore.RequestSpec;
import net.momoka.eeyore.ResponseSpec;

public interface BaseImpl {

  public byte[] sendRequest(
    MobileApp app, RequestSpec spec, List<String> idfas);

  public Map<String, Integer> handleResponse(
    MobileApp app, ResponseSpec spec, byte[] body);

}
