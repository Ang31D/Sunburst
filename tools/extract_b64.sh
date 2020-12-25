#!/bin/bash

if [[ -p "/dev/stdin" ]]; then
   cat "/dev/stdin" | tr " " "\n" | grep -Eo 'Unzip\("(.+)"\)' | sed 's/Unzip("//g' | sed 's/")$//g'
elif [[ "${#1}" > 0 ]]; then
   cat "$1" | tr " " "\n" | grep -Eo 'Unzip\("(.+)"\)' | sed 's/Unzip("//g' | sed 's/")$//g'
fi
