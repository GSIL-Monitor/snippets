package net.momoka.jetty;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import freemarker.template.TemplateException;
import freemarker.template.TemplateNotFoundException;
import freemarker.template.MalformedTemplateNameException;

public class BaseServlet extends HttpServlet {

  private HttpServletRequest req;
  private HttpServletResponse resp;

  protected Object get(
    HttpServletRequest req, HttpServletResponse resp) {
    throw new UnsupportedOperationException();
  }

  protected Object post(
    HttpServletRequest req, HttpServletResponse resp) {
    throw new UnsupportedOperationException();
  }

  protected Object put(
    HttpServletRequest req, HttpServletResponse resp) {
    throw new UnsupportedOperationException();
  }

  protected Object delete(
    HttpServletRequest req, HttpServletResponse resp) {
    throw new UnsupportedOperationException();
  }

  protected Object head(
    HttpServletRequest req, HttpServletResponse resp) {
    throw new UnsupportedOperationException();
  }

  protected Object option(
    HttpServletRequest req, HttpServletResponse resp) {
    throw new UnsupportedOperationException();
  }

  @Override
  protected void doGet(HttpServletRequest req, HttpServletResponse resp)
    throws ServletException, IOException {

    this.req = req;
    this.resp = resp;

    req.setCharacterEncoding("utf-8");
    resp.setCharacterEncoding("utf-8");

    resp.setHeader("Content-Type", "text/plain");

    PrintWriter pw = resp.getWriter();

    Object result = get(req, resp);

    pw.write(result.toString());
  }

  @Override
  protected void doPost(HttpServletRequest req, HttpServletResponse resp)
    throws ServletException, IOException {

    this.req = req;
    this.resp = resp;

    req.setCharacterEncoding("utf-8");
    resp.setCharacterEncoding("utf-8");

    resp.setHeader("Content-Type", "text/plain");

    PrintWriter pw = resp.getWriter();

    Object result = post(req, resp);

    pw.write(result.toString());
  }

  protected String renderTemplate (String name, Object dataModel) {

    resp.setHeader("Content-Type", "text/html");
    StringWriter writer = new StringWriter();

    try {
      TemplateLoader.getInstance().render(name,  dataModel, writer);
    }
    catch (MalformedTemplateNameException e) {
      e.printStackTrace();
    }
    catch (TemplateException e) {
      e.printStackTrace();
    }
    catch (TemplateNotFoundException e) {
      e.printStackTrace();
    }
    catch (IOException e) {
      e.printStackTrace();
    }

    return writer.toString();

  }

}
