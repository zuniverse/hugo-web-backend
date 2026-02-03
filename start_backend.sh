#!/bin/bash 

# -x : Print a trace of simple commands
# -e : Exit immediately if a pipeline returns a non-zero status.
set -ex

source "venv/bin/activate"

# check i'm in good venv
echo $VIRTUAL_ENV

python3 -m flask --env-file .env run
python3 -m flask run
