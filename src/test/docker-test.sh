#!/usr/bin/env bash

mkdir -p bcp
mkdir -p logs

docker run --rm \
  --name database-table-copy \
  --mount type=bind,source="$(pwd)",target=/config \
  --mount type=bind,source="$(pwd)/bcp",target=/app/bcp \
  --mount type=bind,source="$(pwd)/logs",target=/app/logs \
  wolfyreload/database-table-copy:latest \
  /config/config.json
