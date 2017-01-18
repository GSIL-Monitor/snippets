<?php

namespace App\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;

class Kernel extends ConsoleKernel
{

    protected $commands = [
        RabbitMQ\Consumer::class,
    ];

    protected function schedule(Schedule $schedule) {

    }

}