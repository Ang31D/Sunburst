#!/bin/bash

script_pwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
tools_dir=$(echo "$script_pwd")

if [[ -p "/dev/stdin" ]]; then
   cat "/dev/stdin" | while read value; do hash=$(echo "$value" | python3 $tools_dir/dencode.py -H); echo "${hash} ${value}"; done
else
   value=$(echo "$1")
   hash=$(echo "$value" | python3 $tools_dir/dencode.py -H)
   echo "${hash} ${value}"
fi
