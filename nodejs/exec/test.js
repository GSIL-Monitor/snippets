var exec = require('child_process').exec;

child = exec('sudo -u nobody -H ids', function(error, stdout, stderr) {
  if (error != null) {
    console.log(error);
    return;
  }

  console.log(stdout);
  console.log(stderr);

});
