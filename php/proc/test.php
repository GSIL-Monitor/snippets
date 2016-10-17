<?php

function subprocess($cmd, $cwd = "./", $env = array()) {
    $descriptorspec = array(
        0 => array("pipe", "r"),
        1 => array("pipe", "w"),
        2 => array("pipe", "w"),
    );

    $process = proc_open($cmd, $descriptorspec, $pipes, $cwd, $env);

    if (is_resource($process)) {
        $stdout = stream_get_contents($pipes[1]);
        $stderr = stream_get_contents($pipes[2]);
        fclose($pipes[0]);
        fclose($pipes[1]);
        fclose($pipes[2]);
        $ret = proc_close($process);
        $rv = array(
            'ret' => $ret,
            'stdout' => $stdout,
            'stderr' => $stderr
        );
        return $rv;
    }
    else {
        throw new Exception();
    }
}

$o = subprocess("/bin/bash a.sh");

var_dump($o);
