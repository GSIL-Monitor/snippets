<?php

// I know, I know, there are proc_open, exec, system functions to use.
// But they just suck...
// So I wrote this, hope this will help ourselves out :3

function subprocess($cmd, $login = FALSE, $cwd = './',
                    $shell = '/bin/bash', $pipespec = NULL) {

    $pid = getmypid();

    // avoid concurrency problems (for parent processes)
    $inpipe = '/tmp/_php_inpipe' . $pid;
    $outpipe = '/tmp/_php_outpipe' . $pid;
    $errpipe = '/tmp/_php_errpipe' . $pid;
    if ($pipespec) {
        $inpipe = $pipespec['stdin'];
        $outpipe = $pipespec['stdout'];
        $errpipe = $pipespec['stderr'];
    }

    posix_mkfifo($inpipe, 0600);
    posix_mkfifo($outpipe, 0600);
    posix_mkfifo($errpipe, 0600);

    $pid = pcntl_fork();

    if ($pid) {
        // parent
        $ret = 0;

        $out = fopen($outpipe, 'r');
        $err = fopen($errpipe, 'r');

        while (TRUE) {
            $_ = pcntl_waitpid($pid, $status, WNOHANG);
            
            if ($_ === 0) {
                usleep(1000);
            }
            elseif (pcntl_wifexited($status)) {
                $ret = pcntl_wexitstatus($status);
                break;
            }
            else {
                throw new RuntimeException();
            };
        }

        $_stdout = '';
        $_stderr = '';
        while (!feof($out)) {
            $_stdout .= fgets($out);
        }

        
        while (!feof($err)) {
            $_stderr .= fgets($err);
        }

        fclose($out);
        fclose($err);
        
        unlink($inpipe);
        unlink($outpipe);
        unlink($errpipe);
        $rv = array(
            'ret' => $ret,
            'stdout' => $_stdout,
            'stderr' => $_stderr,
        );
        return $rv;
    }
    else {
        if ($cwd) {
            chdir($cwd);
        }
        $params = array('-c', "$cmd >${outpipe} 2>${errpipe}");
        if ($login) {
            array_unshift($params, '-l');
        }
        pcntl_exec($shell, $params);
    }
}

$_ = subprocess("git achie | bzip2 - ", TRUE);

var_dump($_);
