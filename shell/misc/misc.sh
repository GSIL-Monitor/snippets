#!/bin/bash

function a () {
  return 0
}

if a; then
  echo 1
else
  echo 2
fi
