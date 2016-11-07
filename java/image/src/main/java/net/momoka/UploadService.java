package net.momoka;

import java.io.InputStream;

public interface UploadService {

  boolean upload(String filename, InputStream is);

}
