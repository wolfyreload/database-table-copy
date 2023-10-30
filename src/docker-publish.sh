#!/usr/bin/env bash

# set push to 0 if no argument is provided
push=${1-0}

version=$(git describe --tags)

docker build . -t "wolfyreload/database-table-copy:latest"
docker tag "wolfyreload/database-table-copy:latest" "wolfyreload/database-table-copy:${version}"

if [ "$push" -eq 1 ]; then
  echo "pushing to dockerhub"
  docker push "wolfyreload/database-table-copy:latest"
  docker push "wolfyreload/database-table-copy:${version}"
fi