package net.momoka.controller;

import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.InputStream;
import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.util.ArrayList;
import java.util.List;
import javax.annotation.Resource;
import javax.imageio.ImageIO;

import com.qianka.util.DigestUtil;
import com.qianka.util.ImageUtil;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
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

import net.momoka.APIResult;
import net.momoka.DataResult;
import net.momoka.UploadResult;
import net.momoka.UploadService;

@Controller
public class UploadController {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(UploadController.class);

  @Resource
  private UploadService uploadService;

  @PostMapping("/uploadFile/{namespace}")
  @ResponseBody
  public APIResult uploadFileWithNamespace(
    @PathVariable("namespace") String namespace,
    @RequestParam(name = "file", required = true)
    MultipartFile file) throws IOException {
    InputStream is = file.getInputStream();

    LOGGER.debug("{}", file);
    return doUpload(namespace, is);
  }

  @PostMapping("/uploadFile")
  @ResponseBody
  public APIResult uploadFile(
    @RequestParam(name = "file", required = true)
    MultipartFile file) throws IOException {
    InputStream is = file.getInputStream();

    LOGGER.debug("{}", file);
    return doUpload("", is);
  }

  @PostMapping("/upload/{namespace}")
  @ResponseBody
  public APIResult uploadWithNamespace(
    @PathVariable("namespace") String namespace,
    @RequestBody byte[] body) throws IOException {

    InputStream is = new ByteArrayInputStream(body);
    return doUpload(namespace, is);
  }

  @PostMapping("/upload")
  @ResponseBody
  public APIResult upload(
    @RequestBody byte[] body) throws IOException {

    InputStream is = new ByteArrayInputStream(body);
    return doUpload("", is);
  }

  private APIResult doUpload(
    String namespace, InputStream is) throws IOException {
    APIResult rv = new APIResult();
    UploadResult result = new UploadResult();

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

    bis.reset();

    byte[] b = new byte[av];
    bis.read(b, 0, av);
    bis.reset();
    ByteArrayInputStream bais = new ByteArrayInputStream(b);

    String format = mime.toLowerCase().substring(6);
    result.setFormat(format);
    LOGGER.debug("format: {}", format);
    BufferedImage im = ImageIO.read(bais);
    bais.close();
    result.setHeight(im.getHeight());
    result.setWidth(im.getWidth());

    List<DataResult> results = new ArrayList<DataResult>();
    results.add(result);

    String filename = md5 + "." + format;
    if (namespace != null && namespace.length() > 0) {
      filename = namespace.replaceAll("\\/+$", "") + "/" + filename;
    }

    result.setFilename(filename);


    boolean ok = uploadService.upload(filename, bis);

    if (!ok) {
      rv.setStatus("error");
      rv.setErrorMessage("upload failed");
      return rv;
    }

    // upload
    rv.setStatus("ok");
    rv.setData(results);
    return rv;
  }

}
