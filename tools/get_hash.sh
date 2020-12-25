#!/bin/bash

script_pwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
hashes_dir=$(echo "$script_pwd/../hashes")

value=$(echo "$1")
hash=$(echo "$value" | tr '[:upper:]' '[:lower:]' | python3 $script_pwd/dencode.py -H)

hash_file=$(echo "$hashes_dir/hashcat_team.cracked_hashes.txt")
if [[ "${#2}" > 0 ]]; then
   hash_file=$(echo "$2")
fi

match=$(grep -E "^${hash} | ${hash}$" $hash_file)

if [[ "${#match}" > 0 ]]; then
   echo "${match}"
fi
