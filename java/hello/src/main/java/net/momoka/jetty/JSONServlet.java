package net.momoka.jetty;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.json.simple.JSONValue;

public class JSONServlet extends BaseServlet {

    protected Object get(HttpServletRequest req, HttpServletResponse resp) {
        throw new UnsupportedOperationException();
    }

    protected Object post(HttpServletRequest req, HttpServletResponse resp) {
        throw new UnsupportedOperationException();
    }

    protected Object put(HttpServletRequest req, HttpServletResponse resp) {
        throw new UnsupportedOperationException();
    }

    protected Object delete(HttpServletRequest req, HttpServletResponse resp) {
        throw new UnsupportedOperationException();
    }

    protected Object head(HttpServletRequest req, HttpServletResponse resp) {
        throw new UnsupportedOperationException();
    }

    protected Object option(HttpServletRequest req, HttpServletResponse resp) {
        throw new UnsupportedOperationException();
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {

        req.setCharacterEncoding("utf-8");
        resp.setCharacterEncoding("utf-8");

        resp.setHeader("Content-Type", "application/json");

        PrintWriter pw = resp.getWriter();

        Object result = get(req, resp);

        String out = JSONValue.toJSONString(result);

        pw.write(out);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {

        req.setCharacterEncoding("utf-8");
        resp.setCharacterEncoding("utf-8");

        resp.setHeader("Content-Type", "application/json");

        PrintWriter pw = resp.getWriter();

        Object result = post(req, resp);

        String out = JSONValue.toJSONString(result);

        pw.write(out);
    }

}
