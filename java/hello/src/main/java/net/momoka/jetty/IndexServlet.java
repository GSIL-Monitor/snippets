package net.momoka.jetty;

import java.util.Map;
import java.util.TreeMap;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class IndexServlet extends BaseServlet {

  @Override
  protected Object get(HttpServletRequest req, HttpServletResponse resp) {

    // return "hello world";

    Map<String, Object> model = new TreeMap<String, Object>();
    model.put("message", "Hello, Freemarker!");

    String output = renderTemplate("index.html", model);
    return output;

  }

}
