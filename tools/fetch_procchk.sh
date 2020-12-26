#!/bin/bash

script_pwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
tools_dir=$(echo "$script_pwd")

work_dir=$(mktemp -d -t ci-XXXXXXXXXX)
if [[ "${#1}" > 0 ]]; then
   url=$(echo "$1")
   wget -q $url -O $work_dir/tmp.html
   # // fetch process html section
   num=$(cat $work_dir/tmp.html | grep -En "<table|<\/table" | sed 's/:.*//g' | tr '\n' ',' | sed 's/,$//g')
   start=$(echo $num | cut -d, -f 1)
   end=$(echo $num | cut -d, -f 2)
   sed -n "${start},${end}p" $work_dir/tmp.html > $work_dir/tmp.html.section
   # // hash file(s) name
   cat $work_dir/tmp.html.section | grep -E "<td><a " | sed 's/.*html">//g' | sed 's/<\/a>.*//g' | $tools_dir/tolower.sh | $tools_dir/basename.sh | sort -u > $work_dir/tmp.result
   # // hash file(s) description
   cat $work_dir/tmp.html.section | grep -E "<td> " | sed 's/.*<td> //g' | sed 's/<\/td>.*//g' | sort -u | grep -Ev "^$" | $tools_dir/tolower.sh >> $work_dir/tmp.result
   # // output result
   cat $work_dir/tmp.result | sort -u | $tools_dir/hash_value.sh | sort -u
   # // clean-up
   rm -rf $work_dir
fi
