<?php

return [
    "connections" => [
        "default" => [
            "host" => env("RABBITMQ_HOST", "127.0.0.1"),
            "port" => env("RABBITMQ_PORT", 5672),
            "username" => "guest",
            "password" => "guest",
            "vhost" => "/",
            "heartbeat_interval" => env("RABBITMQ_HEARTBEAT", 120),
        ],
    ],
];
