#!/bin/sh

config_path=$1
script_arguments=${@:2}

if [ "$IMAGE_NAME" == "" ];
then
    docker-compose -f $config_path run --rm train
else
    docker-compose -f $config_path run --rm train script_arguments
fi
