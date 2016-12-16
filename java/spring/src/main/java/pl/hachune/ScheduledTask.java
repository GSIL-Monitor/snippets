package pl.hachune;

import java.util.Date;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ScheduledTask {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(ScheduledTask.class);

  @Scheduled(fixedRate = 5000)
  public void reportCurrentTime() {
    LOGGER.debug("{}", new Date());
  }
}
