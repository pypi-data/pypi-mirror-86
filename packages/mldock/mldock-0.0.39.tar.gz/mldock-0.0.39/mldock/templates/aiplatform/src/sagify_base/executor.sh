#!/usr/bin/env bash

function startup (){
    python opt/ml/src/sagify_base/startup.py
}

function cleanup (){
    python opt/ml/src/sagify_base/cleanup.py
}

# start up
startup

exec "$@"

# trap SIGTERM
# trap 'exit 0' SIGTERM

# clean up

cleanup

echo "Complete!"