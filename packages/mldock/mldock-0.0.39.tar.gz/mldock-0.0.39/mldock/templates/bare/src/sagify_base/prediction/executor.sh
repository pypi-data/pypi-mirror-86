#!/usr/bin/env bash

function startup (){
    python src/sagify_base/prediction/startup.py --env='prod'
}

startup

exec "$@"

echo "Complete!"
