package net.momoka.email;

import org.apache.commons.mail.DefaultAuthenticator;
import org.apache.commons.mail.EmailException;
import org.apache.commons.mail.SimpleEmail;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) throws EmailException {


    SimpleEmail mail = new SimpleEmail();

    LOGGER.debug("{}", mail);

    mail.setHostName("smtp.exmail.qq.com");
    // mail.setSmtpPort("");
    mail.setAuthenticator(
      new DefaultAuthenticator(
        "postmaster@qianka.com", "QIANKApassw0rd"));

    mail.setSSLOnConnect(true);

    mail.setFrom("OPS <postmaster@qianka.com>");
    mail.setSubject("just a test subject");
    mail.setMsg("just a test body");
    mail.addTo("chen.lei@qianka.com");
    String messageId = mail.send();
    LOGGER.debug("{}", messageId);

  }

}
