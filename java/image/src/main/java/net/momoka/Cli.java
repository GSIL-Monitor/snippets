package net.momoka;

import java.io.IOException;
import java.io.InputStream;
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;

import com.aliyun.oss.OSSClient;
import com.aliyun.oss.model.PutObjectResult;
import net.sf.jmimemagic.Magic;
import net.sf.jmimemagic.MagicException;
import net.sf.jmimemagic.MagicMatchNotFoundException;
import net.sf.jmimemagic.MagicParseException;



import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.qianka.util.IOUtil;
import com.qianka.util.ImageUtil;
import com.qianka.util.DigestUtil;

public class Cli {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(Cli.class);

  public Cli() {

  }

  public static void main(String[] args) throws Throwable {
    InputStream is = new BufferedInputStream(
      new FileInputStream(System.getProperty("file")));

    int av = is.available();
    is.mark(av);
    boolean image = ImageUtil.isImage(is);
    if (!image) {
      LOGGER.debug("not an image");
      return;
    }

    is.reset();

    String mime = ImageUtil.detect(is);
    LOGGER.debug("type: {}", mime);
    is.reset();

    String md5 = DigestUtil.md5sum(is);
    LOGGER.debug("md5: {}", md5);
    is.reset();

    FileOutputStream os = new FileOutputStream("test");

    for (int i = 0; i < av; i++) {
      os.write(is.read());
    }

    is.reset();

    upload(md5, is);

    os.close();
    is.close();
  }

  private static void upload(String filename, InputStream is) {
    String endpoint = "http://oss-cn-hangzhou.aliyuncs.com";
    String accessId = System.getProperty("access.id");
    String accessSecret = System.getProperty("access.secret");
    String bucket = System.getProperty("bucket");

    OSSClient client = new OSSClient(
      endpoint, accessId, accessSecret);

    PutObjectResult result = client.putObject(bucket, filename, is);
    // client.deleteObject(bucket, filename);

    String etag = result.getETag();
    LOGGER.debug("etag: {}", etag);

    client.shutdown();
  }
}
