const express = require('express');
const app = express();
const port = 3000;

app.get('/', function (req, resp) {
  resp.send('hello world!');
});

app.listen(port, function () {
  console.log('Example app is listening on port ' + port);
});
