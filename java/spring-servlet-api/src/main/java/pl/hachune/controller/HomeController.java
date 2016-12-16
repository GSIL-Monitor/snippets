package pl.hachune.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
@RequestMapping("/")
public class HomeController {

  @RequestMapping(path = {"", "/", "/index"})
  @ResponseBody
  public String home() {
    return "hello world";
  }

}
