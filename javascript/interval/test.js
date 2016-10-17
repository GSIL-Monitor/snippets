var sleep = require('sleep');


function sleepFor30S () {
  console.log('sleeping');
  sleep.sleep(3);

}

setInterval(sleepFor30S, 1000);
setInterval(sleepFor30S, 2000);
