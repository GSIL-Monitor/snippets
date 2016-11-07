package net.momoka;

import java.io.InputStream;
import javax.annotation.Resource;

import com.aliyun.oss.OSSClient;
import com.aliyun.oss.model.PutObjectResult;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class UploadServiceImpl implements UploadService {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(UploadServiceImpl.class);

  @Resource
  private OSSClient oss;

  private String bucket;

  public UploadServiceImpl() {

  }

  public void setBucket(String b) {
    this.bucket = b;
  }

  @Override
  public boolean upload(String filename, InputStream is) {

    if (oss.doesObjectExist(bucket, filename)) {
      LOGGER.info("already exists, skip uploading...");
    }

    PutObjectResult result = oss.putObject(bucket, filename, is);

    String etag = result.getETag();

    if (etag != null && etag.length() > 0) {
      return true;
    }
    return false;
  }

}
