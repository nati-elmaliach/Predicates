#!/bin/bash
set -e

if [ "$1" = "remote" ]; then
    exec python3 src/remote/index.py
elif [ "$1" = "test" ]; then
    exec pytest -v
else
    echo "Invalid argument. Use 'remote' to run the Flask server or 'test' to run the Python script."
    exit 1
fi