#!/bin/bash -eu

echo '{' > misspellings_lib/wikipedia.json


url='http://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines'

# Ignore weird duplicate lines and put them in "custom.json" instead.
curl "$url" 2>| /dev/null \
  | sed -n '/<pre>/,/<\/pre>/p' \
  | sed 's/   */ /g' \
  | sed "s/'/\\\'/g;s/\(.*\)-.gt;\(.*\)/    '\1': ['\2'],/;s/, /', '/g" \
  | sed '1d;$d' \
  | sed "s/'/\"/g" \
  | grep -v "^'ok' " \
  | sed '$s/,$//' \
  | grep -v '"moil"' \
  | grep -v '"refernce"' \
  >> misspellings_lib/wikipedia.json

echo '}' >> misspellings_lib/wikipedia.json
