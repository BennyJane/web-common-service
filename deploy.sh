#!/bin/bash
set -e

cd $(dirname "$0")
echo "[当前目录]： $(pwd)"

`flask db upgrade`
sleep 3
`gunicorn -c gunicorn.conf.py main:app --preload`
