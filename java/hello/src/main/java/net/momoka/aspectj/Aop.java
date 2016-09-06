package net.momoka.aspectj;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Aspect
public class Aop {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Aop.class);

  private boolean evaluated = false;
  private String cached = null;

  public Aop() {

  }

  @Around("execution(* net.momoka.aspectj.Db.getSomething(..))")
  public String getSomething(ProceedingJoinPoint pjp) throws Throwable {

    LOGGER.debug("aop");

    if (evaluated == false) {
      cached = (String) pjp.proceed();
      evaluated = true;
    }
    return cached;
  }

}
