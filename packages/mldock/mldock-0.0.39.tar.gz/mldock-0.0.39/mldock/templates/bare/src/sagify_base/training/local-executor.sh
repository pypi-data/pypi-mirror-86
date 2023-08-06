#!/usr/bin/env bash

function startup (){
    python src/sagify_base/training/startup.py --env="dev"
}

function cleanup (){
    python  src/sagify_base/training/cleanup.py --env="dev"
}

startup

"$@" & 

cleanup

echo "Complete!"