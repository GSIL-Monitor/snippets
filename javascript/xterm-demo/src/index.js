import { Terminal } from 'xterm';
import * as fit from 'xterm/lib/addons/fit/fit';

$(function () {
  Terminal.applyAddon(fit);
  console.log('fit addon applied');
  let el = document.getElementById('terminal');
  let term = new Terminal();
  console.log('terminal created');
  term.open(el);
  console.log('terminal opened');
  term.fit();
  console.log('terminal fitted');
  let cnt = 0;
  let hdl = null;
  let append = function () {
    var d = new Date().toString();
    term.writeln(d);
    cnt++;
    if (cnt > 100 && hdl != null) {
      window.clearInterval(hdl);
    }
  };
  hdl = window.setInterval(append, 10);
});
