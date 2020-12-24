#!/bin/bash

script_pwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
hashes_dir=$(echo "$hash $script_pwd/../hashes")

hash=$(echo "$1")

match=$(grep $hash $hashes_dir/hashcat_team.cracked_hashes.txt)

if [[ "${#match}" > 0 ]]; then
   echo "${match}"
fi
