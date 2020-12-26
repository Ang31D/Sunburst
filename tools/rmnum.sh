#!/bin/bash

script_pwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [[ -p "/dev/stdin" ]]; then
   cat "/dev/stdin" | sed 's/[0-9]//g'
elif [[ "${#1}" > 0 ]]; then
   value=$(echo "$1")
   echo "$value" | sed 's/[0-9]//g'
fi
