#!/bin/sh

config_path=$1

docker-compose -f config_path run --rm --service-ports deploy
