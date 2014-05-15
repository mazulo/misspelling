#!/bin/bash -eu

repository_root=$(dirname "${BASH_SOURCE[0]}")
json_filename="$repository_root/../misspellings_lib/wikipedia.json"

url='http://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines'

{
    echo '{'

    # Ignore weird duplicate lines and put them in "custom.json" instead.
    curl "$url" 2>| /dev/null \
        | sed -n '/<pre>/,/<\/pre>/p' \
        | sed 's/   */ /g' \
        | sed "s/'/\\\'/g;s/\(.*\)-.gt;\(.*\)/    '\1': ['\2'],/;s/, /', '/g" \
        | sed '1d;$d' \
        | sed "s/'/\"/g" \
        | grep -v '"ok"' \
        | sed '$s/,$//' \
        | grep -v '"moil"' \
        | grep -v '"refernce"'

    echo '}'
} > "$json_filename"
