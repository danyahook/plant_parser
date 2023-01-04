#!/bin/bash

set -e

export LANG='en_US.UTF-8'

if [ "$1" = "serve" ] || [ "$1" = "" ]; then
    command="cd /usr/src/plant_parser/src && \
        python run.py"
else
    command="exec sh"
fi

eval "${command}"