package pl.hachune;

import java.util.List;

import com.aliyuncs.IAcsClient;
import com.aliyuncs.ecs.model.v20140526.DescribeInstancesRequest;
import com.aliyuncs.ecs.model.v20140526.DescribeInstancesResponse;
import com.aliyuncs.ecs.model.v20140526.DescribeInstancesResponse.Instance;
import com.aliyuncs.exceptions.ClientException;
import com.aliyuncs.exceptions.ServerException;

import org.springframework.context.annotation.
  AnnotationConfigApplicationContext;
import org.springframework.web.context.support.
  AnnotationConfigWebApplicationContext;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public Main() {

  }

  public static void main(String[] args) throws InterruptedException {

    AnnotationConfigApplicationContext jettyCtx =
      new AnnotationConfigApplicationContext();
    AnnotationConfigApplicationContext ctx =
      new AnnotationConfigApplicationContext();
    AnnotationConfigWebApplicationContext webCtx =
      new AnnotationConfigWebApplicationContext();

    jettyCtx.register(JettyConfig.class);
    jettyCtx.refresh();

    ctx.register(Config.class);
    ctx.refresh();

    webCtx.register(Config.class);
    webCtx.register(WebConfig.class);

    Jetty jetty = jettyCtx.getBean(Jetty.class);
    jetty.setContext(webCtx);
    //jetty.start();
    //webCtx.refresh();

    IAcsClient client = ctx.getBean(IAcsClient.class);
    LOGGER.debug("{}", client);

    YuntongxunNotify y = ctx.getBean(YuntongxunNotify.class);
    boolean rs = y.notify("13818391941", "01234567");
    LOGGER.debug("{}", rs);

    // int page = 1;
    //
    // try {
    //
    //   while (true) {
    //     DescribeInstancesRequest req = new DescribeInstancesRequest();
    //     req.setPageNumber(page);
    //     req.setPageSize(30);
    //
    //     LOGGER.debug("{}", page);
    //     DescribeInstancesResponse resp = client.getAcsResponse(req);
    //     LOGGER.debug("{}", resp);
    //     List<Instance> instances = resp.getInstances();
    //     if (instances.size() <= 0) {
    //       break;
    //     }
    //
    //     for (Instance inst: instances) {
    //       LOGGER.debug("InstanceId: {}", inst.getInstanceId());
    //       LOGGER.debug("InstanceName: {}", inst.getInstanceName());
    //       LOGGER.debug("Hostname: {}", inst.getHostName());
    //       LOGGER.debug("Description: {}", inst.getDescription());
    //       LOGGER.debug("Cpu: {}", inst.getCpu());
    //       LOGGER.debug("Memory: {}", inst.getMemory());
    //       LOGGER.debug("Status: {}", inst.getStatus());
    //       LOGGER.debug("=========");
    //     }
    //
    //     page++;
    //
    //   }
    //
    // }
    // catch (ServerException e) {
    //   e.printStackTrace();
    // }
    // catch (ClientException e) {
    //   e.printStackTrace();
    // }

  }

}
