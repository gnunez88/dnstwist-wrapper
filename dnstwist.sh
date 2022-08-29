#!/usr/bin/env bash
TARGET="${1:?Target domain missing}"

DNSTWIST_FOLDER="$(pwd)/dnstwist"
DNSTWIST_URL="https://github.com/elceef/dnstwist"
DNSTWIST="${DNSTWIST_FOLDER}/dnstwist.py"
RESULTS_FOLDER="$(pwd)/results/$(date +'%Y-%m-%d')"

function suggest_installation () {
    TOOL="${1}"
    echo -e "You need to install \"${TOOL}\"." >&2
    exit 2
}

function install_requirements () {
    pip3 install -r dnstwist/requirements.txt
}

#[ -d venv ] \
#    && source venv/bin/activate \
#    || echo -e "Virtual environment (venv) directory not found." >&2 \
#    && echo -e "run: virtualenv -p $(which python3) venv" >&2 \
#    && exit 1

# Check if the venv folder exists, it is accessible and readable
# if not, check if virtualenv is installed
# if so, check if the current directory is writable
# then create a virtual environment in venv
if [ -d venv ]; then
    source venv/bin/activate
    CONTINUE="yes"
elif ! command -v virtualenv >/dev/null 2>&1; then
    suggest_installation virtualenv
elif [ -w . ]; then
    virtualenv -p $(which python3) venv
    STATUS="new"
else
    echo -e "It cannot go on." >&2
    exit 3
fi

# Creating the folder where to save the results
if [ ! -d "${RESULTS_FOLDER}" ]; then
    mkdir -p "${RESULTS_FOLDER}"
fi

if [ "${STATUS}" = "new" ]; then
    if [ -d "${DNSTWIST_FOLDER}" ]; then
        install_requirements && CONTINUE="yes"
    else
        git clone --recursive "${DNSTWIST_URL}" dnstwist \
            && install_requirements \
            && CONTINUE="yes"
    fi
fi

# Run the application
if [ "${CONTINUE}" = "yes" ]; then
    python3 "${DNSTWIST}" -wbsram ${TARGET} --tld tld.txt \
        -f json -o "${RESULTS_FOLDER}"/${TARGET}_$(date +"%H%M%S").json
fi
