package net.momoka.ssh;

import java.io.InputStream;
import java.io.PipedInputStream;
import java.io.PipedOutputStream;
import java.util.Properties;

import com.jcraft.jsch.ChannelExec;
import com.jcraft.jsch.ConfigRepository;
import com.jcraft.jsch.IdentityRepository;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.OpenSSHConfig;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.agentproxy.AgentProxyException;
import com.jcraft.jsch.agentproxy.Connector;
import com.jcraft.jsch.agentproxy.ConnectorFactory;
import com.jcraft.jsch.agentproxy.RemoteIdentityRepository;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public Main() {

  }

  public static void main(String[] args) throws Throwable {

    Properties config = new Properties();
    config.put("StrictHostKeyChecking", "no");
    config.put("PreferredAuthentications", "publickey");

    ConnectorFactory cf = ConnectorFactory.getDefault();
    Connector conn = cf.createConnector();
    IdentityRepository identityRepo = new RemoteIdentityRepository(conn);

    JSch jsch = new JSch();
    ConfigRepository configRepo =
      OpenSSHConfig.parseFile("~/.ssh/config");
    jsch.setConfigRepository(configRepo);
    jsch.setIdentityRepository(identityRepo);

    Session session = jsch.getSession("yukari");
    session.setConfig(config);
    session.connect(5000);

    ChannelExec channel = (ChannelExec) session.openChannel("exec");

    PipedOutputStream errPipe = new PipedOutputStream();
    PipedInputStream errIs = new PipedInputStream(errPipe);

    InputStream is = channel.getInputStream();

    channel.setInputStream(null);
    // channel.setErrStream(errPipe);
    channel.setCommand("hostname");
    channel.connect();
    channel.start();
    while(!channel.isEOF())
      Thread.sleep(100);

    int n = is.available();
    byte[] buf = new byte[n];

    for (int i = 0; i < n; i++) {
      buf[i] = (byte) is.read();
    }

    LOGGER.debug(new String(buf));

    is.close();
    errPipe.close();

    channel.disconnect();
    session.disconnect();

  }
}
