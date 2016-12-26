<?php

namespace App\Console;

use Illuminate\Console\Command;
use Monolog\Handler\StreamHandler;

class ConsoleLoggingCommand extends Command
{

    public function __construct() {
        parent::__construct();

        $mono = \Log::getMonolog();
        $mono->setHandlers([new StreamHandler("php://stdout")]);
    }

}
