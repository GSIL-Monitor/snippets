package net.momoka.jetty;

import java.io.IOException;
import java.io.Writer;

import freemarker.template.Configuration;
import freemarker.template.MalformedTemplateNameException;
import freemarker.template.Template;
import freemarker.template.TemplateException;
import freemarker.template.TemplateNotFoundException;

public class TemplateLoader {

  private static TemplateLoader instance;
  Configuration cfg = null;

  public TemplateLoader () {

  }

  public static TemplateLoader getInstance() {

    if (instance != null) {
      return instance;
    }

    instance = new TemplateLoader();
    return instance;
  }

  public void init () {
    cfg = new Configuration(Configuration.VERSION_2_3_23);
    cfg.setClassForTemplateLoading(
      TemplateLoader.class, "/templates/");
  }

  public void render (String name, Object dataModel, Writer out)
    throws MalformedTemplateNameException, TemplateException,
           TemplateNotFoundException, IOException {
    Template tpl = cfg.getTemplate(name);
    tpl.process(dataModel, out);
  }
}
