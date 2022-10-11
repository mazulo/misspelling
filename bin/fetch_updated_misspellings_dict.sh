#!/bin/bash -eu

repository_root=$(dirname "${BASH_SOURCE[0]}")
json_filename="../src/misspelling_lib/assets/wikipedia.json"

url='https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines'

{
  curl "$url" 2>| /dev/null \
      | sed -n '/<pre>/,/<\/pre>/p' \
      | sed 's/   */ /g' \
      | sed 's/"/\\\"/g;s/\(.*\)-.gt;\(.*\)/    "\1": ["\2"],/;s/, /", "/g' \
      | sed '1d;$d' \
      | grep -v '^ *"ok"' \
      | sed '$s/,$//' \
      | grep -v '^ *"moil"' \
      | grep -v '^ *"refernce"'
} > "$json_filename"

$repository_root/format_misspelling_file_into_json.py "$json_filename"
