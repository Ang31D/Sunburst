#!/bin/bash

script_pwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
hashes_dir=$(echo "$script_pwd/../hashes")

value=$(echo "$1")

matches=$(grep -i $value $hashes_dir/hashcat_team.cracked_hashes.txt)

if [[ "${#matches}" > 0 ]]; then
   echo "${matches}"
fi
