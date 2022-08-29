#!/usr/bin/env bash
JSON="${1}"
APP_NAME="$(basename $0)"

function usage () {
    echo -e "Usage: ${APP_NAME} [<path-to-json-file>|<path-to-folder>] [-a]" >&2
    exit 1
}

function parse_file () {
    JSON_FILE="${1}"
    ARG=${2}
    python3 parse-info.py "${JSON_FILE}" ${ARG} | column -t | tr '$' ' '
}

function parse_everything () {
    JSON_DIR="${1}"
    ARG=${2}
    for json_file in $(find ${JSON_DIR} -type f ! -empty | grep '\.json$'); do
        parse_file "${json_file}" ${ARG}; echo
    done
}

if [ $# -eq 0 ]; then
    parse_everything .
elif [ "${1}" = "-a" ]; then
    parse_everything . -a
elif [ "${1}" = "-h" ]; then
    usage
elif [ -d "${JSON}" ]; then
    parse_everything $@
elif [ -f "${JSON}" ]; then
    parse_file $@
fi
