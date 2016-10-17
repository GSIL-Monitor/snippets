<?php

require_once('vendor/autoload.php');

use Symfony\Component\Yaml\Yaml;

$arr = Yaml::parse("a.yaml");

var_dump(Yaml::dump($arr));