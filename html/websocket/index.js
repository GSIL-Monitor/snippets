'use strict';

// var ws = new WebSocket("ws://121.40.218.160:8888/data");
var ws = new WebSocket("ws://127.0.0.1:4444/notify/subscribe");

ws.onmessage = function (event) {
  console.log(event);
};
