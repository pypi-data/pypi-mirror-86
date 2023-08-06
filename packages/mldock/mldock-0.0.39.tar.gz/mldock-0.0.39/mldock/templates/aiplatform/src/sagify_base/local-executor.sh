#!/usr/bin/env bash

function startup (){
    python src/sagify_base/startup.py
}

function cleanup (){
    python src/sagify_base/cleanup.py
}

# start up
startup

exec "$@"

echo "Complete!"