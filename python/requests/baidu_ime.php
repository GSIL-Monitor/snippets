<?php
$strData = file_get_contents('./idfa.txt');
$strTime = time();
$strFrom = '1009309v';
$strToken = 'FpOd2tLRjVaa1FOaU9kTVBpZURPcklBQXZFNnpwM2ZrYXBoWk16';

$strSecret = md5($strFrom . $strTime . $strToken . $strData);
//echo 'curl --header "Content-Type: text/plan"  -X POST -T ./idfa.txt "' . "http://cp01-sys-ra09-jueheng2qa118.cp01.baidu.com:8015/v5/idfa/status?" . "from=" . $strFrom . "&secret=" . $strSecret . "&time=" . $strTime .'"' . "\n";
echo 'curl --header "Content-Type: text/plan"  -X POST -T ./idfa.txt "' . "http://r6.mo.baidu.com/v5/idfa/status?" . "from=" . $strFrom . "&secret=" . $strSecret . "&time=" . $strTime .'"' . "\n";
exit;
