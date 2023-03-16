#!/bin/bash

# usage: compile_all.sh

COMPILER_CMDLINE="g++ -Wall -ansi"

for path in $1/*/$2; do
    basename $(dirname $path)  # group name
    $COMPILER_CMDLINE $path -o ${path%.cpp}
    echo
done