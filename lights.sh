#!/usr/bin/env bash

set -e

#python main.py --layout="4,8,6,5,7" --resolution=0.1 192.168.86.171 "$@"
python main.py --resolution=0.1 192.168.86.171 "$@"
