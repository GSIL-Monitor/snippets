// PhantomJS doesn't support bind yet
Function.prototype.bind = Function.prototype.bind || function (thisp) {
    var fn = this;
    return function () {
	return fn.apply(thisp, arguments);
    };
};
console.log('Loading a web page');
var page = require('webpage').create();
var url = 'http://localhost:8080/#1';
page.open(url, function (status) {
    console.log('Page is loaded!');
    phantom.exit();
});
