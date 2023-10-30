#!/usr/bin/env bash

config_name=${1-config.json}
mkdir -p bcp
mkdir -p logs

docker run --rm \
  --name database-table-copy \
  --mount type=bind,source="$(pwd)",target=/execute \
  wolfyreload/database-table-copy:latest \
  "${config_name}"
