#!/usr/bin/env bash
test_path=$1
tag=$2
image=$3
entrypoint=${4:-"src/sagify_base/training/local-executor.sh"}
cmd=${5:-"python src/sagify_base/training/train.py"}

docker run \
-it \
-v ${test_path}:/opt/ml \
-v /opt/ml \
-p 8080:8080 \
--rm \
--entrypoint "${entrypoint}" \
"${image}:${tag}" \
${cmd}
