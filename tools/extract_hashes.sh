#!/bin/bash

cat "$1" | grep -Eo "[0-9]+UL" | sed 's/UL$//g'
