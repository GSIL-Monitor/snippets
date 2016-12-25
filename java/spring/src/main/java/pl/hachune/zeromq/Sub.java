package pl.hachune.zeromq;

import javax.annotation.PostConstruct;

import org.zeromq.ZMQ;
import org.zeromq.ZMQ.Context;
import org.zeromq.ZMQ.Socket;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Sub {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Sub.class);


  private Context context;
  private Socket subscriber;

  public Sub() {

  }

  @PostConstruct
  public void init() {
    context = ZMQ.context(1);
    subscriber = context.socket(ZMQ.SUB);
    subscriber.connect("tcp://127.0.0.1:5555");
    subscriber.subscribe(ZMQ.SUBSCRIPTION_ALL);
  }

  public String recv() {
    String rv = subscriber.recvStr(0);
    return rv;
  }

}
