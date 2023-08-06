#!/usr/bin/env bash

function startup (){
    python src/sagify_base/training/startup.py --env="prod"
}

function cleanup (){
    python src/sagify_base/training/cleanup.py --env="prod"
}

startup

"$@" & 

wait



cleanup

echo "Complete!"