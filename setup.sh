#!/bin/sh
# Run with `source ./setup.sh` from the project directory so activation stays
# in the current terminal.
python3 -m venv .venv &&
    .venv/bin/python -m pip install -r requirements.txt &&
    . .venv/bin/activate
