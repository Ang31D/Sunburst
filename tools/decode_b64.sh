#!/bin/bash

script_pwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
tools_dir=$(echo "$script_pwd")

if [[ -p "/dev/stdin" ]]; then
   cat "/dev/stdin" | python3 $tools_dir/dencode.py
elif [[ "${#1}" > 0 ]]; then
   echo "$1" | python3 $tools_dir/dencode.py
fi
