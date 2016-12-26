<?php

namespace App\Console\RabbitMQ;

use RabbitMQ;
use Qianka\RabbitMQ\RabbitMQQueue;
use Qianka\RabbitMQ\RabbitMQExchange;
use App\Console\ConsoleLoggingCommand;


class Consumer extends ConsoleLoggingCommand
{

    protected $name = "rabbitmq:consumer";

    protected $consumer = null;

    public function __construct() {
        parent::__construct();
    }

    public function handle() {
        // \Log::info(date("Y-m-d H:i:s"));

        $exchange = new RabbitMQExchange(
            'amq.topic',
            'topic',
            true,       // durable
            false       // auto_delete
        );

        $queue = new RabbitMQQueue(
            'test',
            true,       // durable
            false,      // exclusive
            false,      // auto_delete
            '#'         // routing_key
        );

        $this->consumer = $consumer = RabbitMQ::createConsumerv2(
            $exchange,
            $queue,
            'default',  // connection name in config
            true        // heartbeat
        );

        $consumer->setNetworkRecovery(true);
        $consumer->setTopologyRecovery(true);

        $consumer->setPostErrorHook(function ($e) {
            $this->post_error_hook($e);
        });

        $consumer->consume(
            false,       // no_ack
            false,       // exclusive
            function ($d, $props, $body) {
                $this->process_message($d, $props, $body);
            }
        );

        $consumer->blockingConsume();

    }

    public function post_error_hook($error) {
        \Log::error("running post_error_hook: " . get_class($error));

    }

    public function process_message($d, $props, $body) {
        \Log::info("dinfo: " . var_export($d, 1));
        \Log::info("props: " . var_export($props, 1));
        \Log::info("body: " . var_export($body, 1));
        \Log::info("============");
        $this->consumer->getChannel()->basic_ack($d["delivery_tag"]);
    }

}
