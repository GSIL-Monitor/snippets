<?php

$conf = new Rdkafka\Conf();

$conf->set('queue.buffering.max.ms', 50);

$rk = new Rdkafka\Producer($conf);
$rk->setLogLevel(LOG_DEBUG);
$rk->addBrokers("localhost:9092");

$conf = new RdKafka\Conf();



$topic = $rk->newTopic("test");

for ($i = 0 ; $i < 1000; $i++) {
    $topic->produce(RD_KAFKA_PARTITION_UA, 0, "message payload");
}
