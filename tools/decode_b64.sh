#!/bin/bash

script_pwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
tools_dir=$(echo "$script_pwd")

echo "$1" | python3 $tools_dir/dencode.py
