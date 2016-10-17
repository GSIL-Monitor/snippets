package net.momoka.ploceus;

import pl.hachune.ploceus.CommandResult;
import pl.hachune.ploceus.SSHClient;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public Main() {

  }

  public static void main(String[] args) {
    SSHClient ssh = new SSHClient("ssh://n1386.ops.gaoshou.me");
    CommandResult result = ssh.exec("hostname");
    LOGGER.error(result.getOut().trim());
    ssh.close();
  }
}
