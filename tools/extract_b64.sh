#!/bin/bash

cat "$1" | tr " " "\n" | grep -Eo 'Unzip\("(.+)"\)' | sed 's/Unzip("//g' | sed 's/")$//g'
