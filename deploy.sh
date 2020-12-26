#!/bin/bash

set -e

cd `dirname "$0"`
echo "[当前目录]： $(pwd)"

function init_project() {
  flask db upgrade
  sleep 3
  gunicorn -c gunicorn.conf.py application:app --preload
}

init_project