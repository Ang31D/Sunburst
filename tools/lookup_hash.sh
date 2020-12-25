#!/bin/bash

script_pwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
hashes_dir=$(echo "$hash $script_pwd/../hashes")

hash_file=$(echo "$hashes_dir/hashcat_team.cracked_hashes.txt")
if [[ "${#2}" > 0 ]]; then
   hash_file=$(echo "$2")
fi

if [[ -p "/dev/stdin" ]]; then
   cat "/dev/stdin" | while read hash; do grep -E "^${hash} | ${hash}$" $hash_file; done
elif [[ "${#1}" > 0 ]]; then
   hash=$(echo "$1")
   grep -E "^${hash} | ${hash}$" $hash_file
fi
