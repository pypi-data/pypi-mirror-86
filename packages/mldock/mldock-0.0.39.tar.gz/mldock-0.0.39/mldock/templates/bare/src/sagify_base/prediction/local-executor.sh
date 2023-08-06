#!/usr/bin/env bash

function startup (){
    python src/sagify_base/prediction/startup.py --env='dev'
}

startup

exec "$@"

echo "Complete!"