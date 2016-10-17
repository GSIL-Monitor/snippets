<?php

// define('SHARED_KEY', '$$123456');
define('SHARED_KEY', '05dm49s11209qwpoaslkzxnjue648rhd');

function sign_payload($method, $payload) {
    ksort($payload);

    $_ = $method;
    $_tmp = array();
    foreach ($payload as $k => $v) {
        $_tmp[] = $k . '=' . $v;
    }

    $_ .= implode('+', $_tmp);

    $_ .= SHARED_KEY;
    echo $_, "\n";
    $rv = md5($_);
    return strtoupper($rv);
}

$timestamp = time();
$create_time = date('Y-m-d H:i:s', $timestamp);

$payload = array(
    'timestamp' => time(),
    'qk_id' => 23968411,
    'order_sn' => 'test_order_sn_1',
    'price' => 12.34,
    'status' => 0,
    'commission' => 234.56,
    'create_time' => $create_time,
    'item_num' => 10,
    'item_title' => '测试商品名称001',
    'num_iid' => '测试淘宝商品id001',
    'seller_shop_title' => '测试店铺名称001',
);


$sign = sign_payload('order.push', $payload);

$payload['sign'] = $sign;

var_dump($payload);

$ch = curl_init();
// curl_setopt($ch, CURLOPT_URL, 'http://127.0.0.1:5000/fanli/order.push');
curl_setopt($ch, CURLOPT_URL,
            'http://n1409.ops.gaoshou.me:8000/fanli/order.push');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_VERBOSE, 1);

$res = curl_exec($ch);
$info = curl_getinfo($ch);
curl_close($ch);

// var_dump($info);

if ($info['http_code'] == 200) {
    $rv = json_decode($res);
    // var_dump($rv);
    if ($rv->code == 200) {
    }
}
