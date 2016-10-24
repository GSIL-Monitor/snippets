package net.momoka.controller;

import java.io.IOException;
import java.io.InputStream;
import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import javax.annotation.Resource;

import com.qianka.util.DigestUtil;
import com.qianka.util.ImageUtil;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.qianka.util.DigestUtil;
import com.qianka.util.ImageUtil;

import net.momoka.UploadResult;

@Controller
public class UploadController {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(UploadController.class);

  @PostMapping("/uploadFile")
  @ResponseBody
  public UploadResult uploadFile(
    @RequestParam(name = "file", required = true)
    MultipartFile file) throws IOException {
    InputStream is = file.getInputStream();

    LOGGER.debug("{}", file);
    return _upload(is);
  }

  @PostMapping("/upload")
  @ResponseBody
  public UploadResult upload(
    @RequestBody byte[] body) throws IOException {

    InputStream is = new ByteArrayInputStream(body);
    return _upload(is);
  }

  private UploadResult _upload(InputStream is) throws IOException {
    UploadResult rv = new UploadResult();
    BufferedInputStream bis = new BufferedInputStream(is);
    int av = bis.available();
    bis.mark(av);

    String md5 = DigestUtil.md5sum(bis);
    LOGGER.debug("md5: {}", md5);
    bis.reset();

    String mime = ImageUtil.detect(bis);
    if (mime == null) {
      rv.setStatus("error");
      rv.setErrorMessage("not an image");
      return rv;
    }

    if (!mime.toLowerCase().startsWith("image/")) {
      rv.setStatus("error");
      rv.setErrorMessage("not an image");
      return rv;
    }

    // upload
    rv.setStatus("ok");
    return rv;
  }

}
