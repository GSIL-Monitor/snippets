package pl.hachune.controllers;

import java.util.ArrayList;
import java.util.List;
import javax.annotation.Resource;

import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import pl.hachune.models.APIResult;
import pl.hachune.models.DataResult;
import pl.hachune.models.Person;

@Controller
public class IndexController {

  private static final Logger LOGGER =
    LoggerFactory.getLogger(IndexController.class);

  @Resource
  private List<Person> persons;

  @RequestMapping(value="/", produces={"application/json"})
  @ResponseBody
  public APIResult index() {
    APIResult rv = new APIResult();
    List<DataResult> data = new ArrayList<DataResult>();

    LOGGER.debug("{}", persons);

    for (Person p: persons) {
      data.add(p);
    }

    rv.setData(data);
    return rv;
  }

  @RequestMapping("/")
  public String indexWithView(@ModelAttribute("model") ModelMap model) {

    LOGGER.debug("{}", persons);

    model.addAttribute("persons", persons);
    return "index";
  }

}
