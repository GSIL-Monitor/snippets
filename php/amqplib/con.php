<?php

require_once(__DIR__.'/vendor/autoload.php');

use PhpAmqpLib\Connection\AMQPConnection;
use PhpAmqpLib\Message\AMQPMessage;
use PhpAmqpLib\Exception\AMQPRuntimeException;

define('HOST', '127.0.0.1');
define('PORT', 5670);
define('USER', 'guest');
define('PASS', 'guest');
define('VHOST', '/');

$exchange = 'test.exchange';
$queue = 'test.chenlei';

function connect () {
    while (1) {
        try {
            return new AMQPConnection(
                HOST,
                PORT,
                USER,
                PASS,
                VHOST,
                false,      // $insist
                'AMQPLAIN', // $login_method =
                null,       // $login_response = null,
                'en_US',    // $locale,
                3,          // $connection_timeout
                10,         // $read_write_timeout
                null,       // $context
                false,      // $keepalive
                5);         // $heartbeat
            break;
        }
        catch (Exception $e) {
            echo $e;
            sleep(2);
        }
    }
}
$conn = connect();
$ch = $conn->channel();
// $consumerTag = 'consumer';
/*
  The following code is the same both in the consumer and the producer.
  In this way we are sure we always have a queue to consume from and an
  exchange where to publish messages.
*/
/*
  name: $queue
  passive: false
  durable: true // the queue will survive server restarts
  exclusive: false // the queue can be accessed in other channels
  auto_delete: false //the queue won't be deleted once the channel is closed.
*/
// $ch->queue_declare($queue, false, true, false, false);
/*
  name: $exchange
  type: direct
  passive: false
  durable: true // the exchange will survive server restarts
  auto_delete: false //the exchange won't be deleted once the channel is closed.
*/
// $ch->exchange_declare($exchange, 'topic', false, true, false);
// $ch->queue_bind($queue, $exchange, '#');

function process_message($message) {
    var_dump($message->body);

    $message->delivery_info['channel']->
        basic_ack($message->delivery_info['delivery_tag']);
}

function consume($ch) {
    $ch->basic_consume(
        'test.chenlei',
        '',    // consumer tag
        false, // no local
        false, // no ack
        false, // exclusive
        false, // no wait
        'process_message');
}

consume($ch);
// $ch->close();
// $conn->close();

while (count($ch->callbacks)) {
    try {
        $ch->wait();
    }
    catch (AMQPRuntimeException $e)  {
        sleep(1);
        echo $e, "\n";
        $conn = connect();
        $ch = $conn->channel();
        consume($ch);
    }
}
