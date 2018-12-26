package net.momoka.lzma;

import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.compress.compressors.xz.XZCompressorInputStream;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Main.class);

  public Main() {

  }

  public static void main(String[] args) throws Throwable {

    List<Integer> l = new ArrayList<Integer>();

    FileInputStream fis = new
      FileInputStream(System.getProperty("xzfile"));

    ByteArrayOutputStream bos = new ByteArrayOutputStream();
    XZCompressorInputStream xis = new XZCompressorInputStream(fis);
    byte[] buffer = new byte[32];
    int n = 0;

    while (-1 != (n = xis.read(buffer))) {
      bos.write(buffer, 0, n);
    }
    ;


    xis.close();
    byte[] result = bos.toByteArray();
    bos.close();
    fis.close();

    LOGGER.debug("{}", new String(result));
  }
}
