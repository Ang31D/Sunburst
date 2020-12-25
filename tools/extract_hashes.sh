#!/bin/bash

if [[ -p "/dev/stdin" ]]; then
   cat "/dev/stdin" | grep -Eo "[0-9]+UL" | sed 's/UL$//g'
elif [[ "${#1}" > 0 ]]; then
   cat "$1" | grep -Eo "[0-9]+UL" | sed 's/UL$//g'
fi
