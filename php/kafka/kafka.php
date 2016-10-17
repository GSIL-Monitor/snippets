<?php
// Produce a message

$topic = 'test';

ini_set('date.timezone', 'Asia/Shanghai');

$kafka = new Kafka('localhost:9092',
                   [
                       Kafka::CONFIRM_DELIVERY => Kafka::CONFIRM_OFF,
                       Kafka::RETRY_COUNT => 1,
                       Kafka::RETRY_INTERVAL => 25,
                   ]);

// while (TRUE) {

    $lines = [];
    for ($i = 0; $i < 10000; $i++) {
        $lines[] = date('Ymd H:i:s');
    }

// $kafka->produceBatch($topic, $lines);
    $kafka->produceBatch($topic, $lines);
    $kafka->disconnect(Kafka::MODE_PRODUCER);
    echo "sent\n";
// break;
// }


// //get all the available partitions
// $partitions = $kafka->getPartitionsForTopic($topic);
//
// //use it to OPTIONALLY specify a partition to consume from
// //if not, consuming IS slower. To set the partition:
// $kafka->setPartition($partitions[0]);//set to first partition

//then consume, for example, starting with the first offset, consume 20 messages
// $msg = $kafka->consume($topic, Kafka::OFFSET_BEGIN, 20);

// var_dump($msg);//dumps array of messages
