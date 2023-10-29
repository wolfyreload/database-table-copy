#!/usr/bin/env bash

# Get the directory path of the script file
script_dir=$(dirname "$0")

pushd "${script_dir}" || exit
pipenv install
pipenv run python setup.py build
popd || exit
