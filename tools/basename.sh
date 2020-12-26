#!/bin/bash

script_pwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [[ -p "/dev/stdin" ]]; then
   cat "/dev/stdin" | grep -oP ".*(?=[.])"
elif [[ "${#1}" > 0 ]]; then
   value=$(echo "$1")
   echo "$value" | grep -oP ".*(?=[.])"
fi
