package net.momoka.path;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) {

    String cwd = System.getProperty("user.dir");
    Path path = Paths.get(cwd, "pom.xml");
    File f = new File(path.toString());
    LOGGER.info("pom.xml is file? {}", f.isFile());

  }

}
